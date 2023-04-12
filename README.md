### pythumbnail

Generates thumbnail images for maryland osu (and hopefully later on, other osu scoreposting channels)

### TODO (yeah lotsa stuff):
- generate config.json upon first user installation
    - user input API stuff; client secret/key
    - default template info (later on)
- merge old api stuff
- create working ui
    - input score URL
    - fetch necessary api data
    - display rendered image
    - frequently call image generator to update, then display image
    - add controls for smaller adjustments
        - comment text field
- create working thumbnail generation
    - fetch info from api
    - use that info in elements on the image
        - Map
            - Title
            - Artist
            - Diffname
            - SR
            - BPM
            - BKG (image)
        - Player
            - Name
            - PFP (image)
        - Score
            - Combo
            - Mods (use assets)
            - Rank (use assets)
            - Acc
            - pp
    - Add comment to image
    - Use font from .ttf file (get from eggpin)
- Template style editor
    - Adjust parts of template and export as json
        - Positions of parts of thumbnail
        - Font size, color, etc.
        - Background blurring & position adjust
        - Placing assets
    - Export as either image or template json