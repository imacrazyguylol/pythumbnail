### pythumbnail

Generates thumbnail images for maryland osu (and hopefully later on, other osu scoreposting channels)

### TODO (yeah lotsa stuff):
- Account for artist/title text that's too long for the screen

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
    - [x] fetch info from api
    - use that info in elements on the image
        - Map
            - Title
            - Artist
            - Diffname
            - SR
            - BPM
            - [x] BKG (image)
        - Player
            - Name
            - [x] PFP (image)
        - Score
            - Combo
            - [x] Mods (use assets)
            - [x] Rank (use assets)
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

