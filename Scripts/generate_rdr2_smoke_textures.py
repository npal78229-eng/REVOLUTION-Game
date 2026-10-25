import os
import math
import random

def create_tga_32(filename, width, height, pixel_data):
    """Writes an uncompressed 32-bit BGRA TGA file."""
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    header = bytearray(18)
    header[2] = 2  # Uncompressed true-color
    header[12] = width & 0xFF
    header[13] = (width >> 8) & 0xFF
    header[14] = height & 0xFF
    header[15] = (height >> 8) & 0xFF
    header[16] = 32 # 32 bits per pixel
    header[17] = 8 | (1 << 5) # 8-bit alpha, origin at top-left
    
    with open(filename, 'wb') as f:
        f.write(header)
        f.write(pixel_data)
    print(f"Generated {filename} ({width}x{height}, {len(pixel_data)} bytes)")

def smoothstep(edge0, edge1, x):
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)

def value_noise_2d(x, y, seed=1337):
    # Simple deterministic grid noise
    def hash2d(ix, iy):
        n = (ix * 374761393 + iy * 668265263 + seed * 1274126177) & 0x7FFFFFFF
        n = (n ^ (n >> 13)) * 1274126177
        return ((n ^ (n >> 16)) & 0x7FFFFFFF) / float(0x7FFFFFFF)
    
    x0 = int(math.floor(x))
    y0 = int(math.floor(y))
    x1 = x0 + 1
    y1 = y0 + 1
    
    fx = x - x0
    fy = y - y0
    
    sx = fx * fx * (3.0 - 2.0 * fx)
    sy = fy * fy * (3.0 - 2.0 * fy)
    
    n00 = hash2d(x0, y0)
    n10 = hash2d(x1, y0)
    n01 = hash2d(x0, y1)
    n11 = hash2d(x1, y1)
    
    nx0 = n00 * (1.0 - sx) + n10 * sx
    nx1 = n01 * (1.0 - sx) + n11 * sx
    return nx0 * (1.0 - sy) + nx1 * sy

def fbm_2d(x, y, octaves=4, seed=1337):
    val = 0.0
    amp = 0.5
    freq = 1.0
    for i in range(octaves):
        val += amp * value_noise_2d(x * freq, y * freq, seed + i * 101)
        freq *= 2.0
        amp *= 0.5
    return val

def generate_pyroclastic_puff(filename, size=512):
    """
    Mimics RDR2's ptxu_PyroclasticVolume:
    Clusters 5 spherical volumes with noise perturbations.
    """
    spheres = [
        (0.50, 0.50, 0.35, 1.0),   # Center main billow
        (0.38, 0.42, 0.26, 0.85),  # Left-upper sub-billow
        (0.62, 0.45, 0.28, 0.88),  # Right-upper sub-billow
        (0.44, 0.62, 0.24, 0.78),  # Lower-left puff
        (0.58, 0.60, 0.25, 0.82),  # Lower-right puff
        (0.50, 0.32, 0.22, 0.70),  # Top chimney crest
    ]
    
    pixels = bytearray(size * size * 4)
    idx = 0
    
    for y in range(size):
        ny = y / float(size)
        for x in range(size):
            nx = x / float(size)
            
            # Combine sphere density
            total_density = 0.0
            normal_x = 0.0
            normal_y = 0.0
            
            # Noise perturbation (curl / fbm noise)
            turb = fbm_2d(nx * 6.0, ny * 6.0, octaves=4, seed=42)
            turb_fine = fbm_2d(nx * 14.0, ny * 14.0, octaves=3, seed=99)
            
            # Perturb UV coordinates along gradient
            distort_x = nx + (turb - 0.5) * 0.08
            distort_y = ny + (turb - 0.5) * 0.08
            
            for sx, sy, srad, sweight in spheres:
                dx = distort_x - sx
                dy = distort_y - sy
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < srad:
                    # Pyroclastic sphere density falloff
                    norm_d = dist / srad
                    density = (1.0 - smoothstep(0.0, 1.0, norm_d)) * sweight
                    if density > total_density:
                        total_density = density
                        # Accumulate approximate normal vector
                        if dist > 0.001:
                            normal_x += (dx / dist) * density
                            normal_y += (dy / dist) * density
            
            # Modulate density with fine turbulence
            total_density = total_density * (0.7 + 0.3 * turb_fine)
            
            # Radial edge falloff to ensure clean borders (no square box clipping)
            edge_dx = nx - 0.5
            edge_dy = ny - 0.5
            edge_dist = math.sqrt(edge_dx * edge_dx + edge_dy * edge_dy)
            border_fade = 1.0 - smoothstep(0.38, 0.49, edge_dist)
            alpha = max(0.0, min(1.0, total_density * border_fade))
            
            # Normal map calculation (for RDR2-style directional light rim / silver lining)
            nz = math.sqrt(max(0.0, 1.0 - min(1.0, normal_x * normal_x + normal_y * normal_y)))
            norm_r = int(max(0, min(255, (normal_x * 0.5 + 0.5) * 255)))
            norm_g = int(max(0, min(255, (normal_y * 0.5 + 0.5) * 255)))
            norm_b = int(max(0, min(255, nz * 255)))
            
            # Channels:
            # B: Normal X / Blue
            # G: Normal Y / Green
            # R: Normal Z / Red
            # A: Density Alpha
            pixels[idx] = norm_b       # B
            pixels[idx + 1] = norm_g   # G
            pixels[idx + 2] = norm_r   # R
            pixels[idx + 3] = int(alpha * 255) # A
            idx += 4
            
    create_tga_32(filename, size, size, pixels)

def generate_curl_noise_flow(filename, size=512):
    """
    Mimics RDR2's ptxu_Noise_m_curlNoiseStrengthKFP:
    Computes mathematical curl: (dNoise/dy, -dNoise/dx) for divergence-free fluid vortices.
    """
    pixels = bytearray(size * size * 4)
    idx = 0
    eps = 1.0 / float(size)
    
    for y in range(size):
        ny = y / float(size)
        for x in range(size):
            nx = x / float(size)
            
            scale = 4.0
            # Compute finite differences for curl
            n_up = fbm_2d(nx * scale, (ny + eps) * scale, octaves=3, seed=777)
            n_dn = fbm_2d(nx * scale, (ny - eps) * scale, octaves=3, seed=777)
            n_rt = fbm_2d((nx + eps) * scale, ny * scale, octaves=3, seed=777)
            n_lf = fbm_2d((nx - eps) * scale, ny * scale, octaves=3, seed=777)
            
            # Curl = (dF/dy, -dF/dx) -> mathematically divergence free (no sinks/sources, pure vortex rolls)
            curl_x = (n_up - n_dn) / (2.0 * eps)
            curl_y = -(n_rt - n_lf) / (2.0 * eps)
            
            # Normalize and pack into [0, 255]
            mag = math.sqrt(curl_x * curl_x + curl_y * curl_y)
            if mag > 0.001:
                curl_x /= mag
                curl_y /= mag
            
            r_byte = int(max(0, min(255, (curl_x * 0.5 + 0.5) * 255)))
            g_byte = int(max(0, min(255, (curl_y * 0.5 + 0.5) * 255)))
            b_byte = int(max(0, min(255, fbm_2d(nx * 8.0, ny * 8.0, octaves=2, seed=333) * 255)))
            a_byte = 255
            
            pixels[idx] = b_byte
            pixels[idx + 1] = g_byte
            pixels[idx + 2] = r_byte
            pixels[idx + 3] = a_byte
            idx += 4
            
    create_tga_32(filename, size, size, pixels)

if __name__ == "__main__":
    out_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Content\VFX\Smoke\Textures"
    generate_pyroclastic_puff(os.path.join(out_dir, "T_Smoke_Pyroclastic_Puff.tga"), size=512)
    generate_curl_noise_flow(os.path.join(out_dir, "T_Smoke_CurlNoise_Flow.tga"), size=512)
