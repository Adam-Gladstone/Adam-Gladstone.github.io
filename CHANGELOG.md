# Issues
- Investigate why giscus comments are not appearing. Resolved by replacing giscus with utterances.

# Wishlist
- Add support for Google Analytics. Unnecessary until there is more traffic.

# Changes

## 28-10-2023
- Changed theme from 'dirt' to 'air'
- Updated link to R-bloggers
- Moved additional pages (About, History) into _pages subdirectory. These are indirectly linked via the masthead (`navigation.yml`) entries. For example, the entry: `url: /about/` references a file `about.md` located in the _pages directory.
- copied _sass into root directory; updated the font sizes.
- Updated bio.

## 29-10-2023
- Removed giscus support. Currently the `comments.html` file does not appear to output the comments section in posts. Tested this by adding a copy of the `single.html` page in the local `_layouts` directory and manually injecting the comments script - this works.
- Added support for utterances. Install the app, update the `_config.yml` file and it works 'out of the box'. No reactions though.

## 03-11-2023
- Updated the website title and about.md
- Added logo

## 10/11/2023
- Added 'excerpt' tag to YAML front matter.