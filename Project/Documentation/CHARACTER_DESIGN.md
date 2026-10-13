# Character Design - Kabir (working brief)

Status: PLACEHOLDER. Kabir is the Manny mannequin (SKM_Manny + ABP_Manny) on BP_Kabir. No final character art exists.

## Role
Ordinary Indian boy whose childhood at home and in the mohalla comes before he discovers colonial oppression and develops a dream of freedom. Protagonist of REVOLUTION.

## Current implementation
- BP_Kabir: RevolutionCharacter parent; third-person camera boom and follow camera; move, look, jump, sprint, crouch, interact input actions.
- IA_Sprint (Left Shift / left stick), IA_Crouch (Left Ctrl / C / right face button), IA_Interact (E / left face button).

## Costume plan (to confirm with owner; period not yet fixed)
- Everyday clothing: simple cotton kurta and dhoti or half-pants in undyed or indigo tones. Colour palette placeholders already exist as M_ClothIndigo_PBR and M_ClothSaffron_PBR.
- Keep silhouette readable at distance: no dark clothing on dark backgrounds.
- Footwear: bare or simple leather chappals.

## Not done / needs decision
- Final face, body, hair, and skin models (needs artist or purchased asset, pending owner approval).
- Costume materials on the mannequin (needs material instance work; not yet assigned).
- Facial animation, voice, and cutscene acting.
- Confirm period and region before finalising costume (see HISTORICAL_REFERENCE_NOTES.md).

## Update 2026-10-12 - first costume step
- Period direction decided: fictional rural UP, c. 1910-1920 (see PROJECT_DIRECTION.md).
- Created M_ClothUndyedCotton_PBR (flat undyed cream-tan colour, matte) in /Game/Environment/Mohalla/Materials.
- Set as the torso-slot material override on BP_Kabir (slot 0). The SKM_Manny asset and its original MI_Manny_02 are unchanged; the override can be removed from BP_Kabir to restore them.
- Legs and head (slot 1, MI_Manny_01) left as-is: they share one material with skin, so changing it would colour the skin.
- Not done: indigo dhoti or half-pants (needs separate leg geometry or a costume mesh); final design (Antigravity or artist); the mannequin body is still an adult-proportioned placeholder.
- NOT verified on screen: the colour and how it reads in Play. Owner to check.
