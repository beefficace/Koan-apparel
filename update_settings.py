import json

def update_settings():
    try:
        with open('config/settings_data.json', 'r') as f:
            data = json.load(f)

        # 1. Typography
        # Note: In a real scenario, we'd pick the exact font handle.
        # Since I can't browse the font picker API, I will set descriptive placeholders
        # or common handles if I knew them. 'playfair_display_n4' and 'inter_n4' are guesses,
        # but often these need to be selected in the editor.
        # However, for the purpose of "initializing" the json, I will set them.
        # If they are invalid, Shopify might fallback to system fonts, which is fine for now.
        # But wait, the user asked for "code ... to initialize this look".
        # If I change settings_data.json, I am initializing it.

        # Actually, "assistant_n4" is the default.
        # I will attempt to set them to the requested families.
        # Font handles in Shopify usually look like 'family_style_weight'.
        # e.g. 'playfair_display_n4' (normal 400), 'inter_n4'.

        data['current']['type_header_font'] = 'playfair_display_n4'
        data['current']['type_body_font'] = 'inter_n4'

        # 2. Color Palette
        # Background: Off-White (#FAFAFA)
        # Text: Soft Black (#1A1A1A)
        # Accents: Urban Red (#D32F2F)

        # I need to update the schemes. Let's update "scheme-1" (default) and "background-1" (old name if exists).
        # In the file I read, I see "color_schemes": { "background-1": ..., "scheme-1": ... }
        # It seems to have both old and new formats or multiple schemes.

        # Let's update 'scheme-1' which is used in 'Default' preset and likely the active one.
        if 'scheme-1' in data['presets']['Default']['color_schemes']:
             scheme = data['presets']['Default']['color_schemes']['scheme-1']['settings']
             scheme['background'] = '#FAFAFA'
             scheme['text'] = '#1A1A1A'
             scheme['button'] = '#D32F2F'
             scheme['button_label'] = '#FFFFFF'
             scheme['secondary_button_label'] = '#1A1A1A'
             # Shadow?
             scheme['shadow'] = '#1A1A1A'

        # Also update 'current' -> 'color_schemes' -> 'background-1' (which seems to be used in 'current')
        if 'background-1' in data['current']['color_schemes']:
             scheme = data['current']['color_schemes']['background-1']['settings']
             scheme['background'] = '#FAFAFA'
             scheme['text'] = '#1A1A1A'
             scheme['button'] = '#D32F2F'
             scheme['button_label'] = '#FFFFFF'
             scheme['secondary_button_label'] = '#1A1A1A'

        # Update 'scheme-1' in current as well if it exists
        if 'scheme-1' in data['current'].get('color_schemes', {}):
             scheme = data['current']['color_schemes']['scheme-1']['settings']
             scheme['background'] = '#FAFAFA'
             scheme['text'] = '#1A1A1A'
             scheme['button'] = '#D32F2F'
             scheme['button_label'] = '#FFFFFF'
             scheme['secondary_button_label'] = '#1A1A1A'

        # 3. Mobile Architecture / Layout
        # Grid spacing.
        # User wants "generous (lots of whitespace/breathing room)".
        # Defaults are 8px. Let's increase to maybe 20px or 24px.
        data['current']['spacing_grid_horizontal'] = 20
        data['current']['spacing_grid_vertical'] = 20
        data['current']['spacing_sections'] = 36 # More breathing room between sections

        # 4. Buttons
        # "Global button styles utilize a 2px border-radius" (from memory)
        # "Primary buttons solid red (#CC2828) and secondary buttons outlined in anthracite (#1A1A1A)."
        # User request: "Accents: ... Urban Red (#D32F2F)".
        # Let's set buttons_radius to 2.
        data['current']['buttons_radius'] = 2
        data['current']['buttons_border_thickness'] = 1 # Keep border thickness for outlined?

        # Save
        with open('config/settings_data.json', 'w') as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"Error: {e}")

update_settings()
