# Kyle Parker Cunningham - Zola Portfolio Site

This is a Zola static site implementation for kyleparkercunningham.com, converted from Ghost CMS.

## Site Structure

```
kpc-site/
├── config.toml              # Zola configuration
├── content/                 # All site content in Markdown
│   ├── _index.md           # Homepage
│   ├── about/              # About page
│   ├── cinema/             # Cinema section  
│   └── oeuvre/             # Artwork catalog
│       ├── _index.md       # Artwork index
│       ├── painting/       # Paintings by year
│       └── printmaking/    # Printmaking works by year
├── static/                 # Static files (images, CSS)
│   ├── images/             # Artwork images organized by date
│   └── style.css           # Generated from SASS
├── templates/              # HTML templates
└── sass/                   # SCSS source files
```

## Features

- **Minimal vanilla CSS**: No frameworks, clean and lightweight
- **Mobile-responsive**: Works on all screen sizes  
- **Fast loading**: Static files, minimal dependencies
- **Easy maintenance**: Pure Markdown content files
- **Long-term preservation**: Standard formats (HTML, CSS, Markdown)

## Development

### Build the site:
```bash
cd kpc-site
zola build
```

### Run local development server:
```bash
cd kpc-site
zola serve
```

Visit http://localhost:1111 to preview the site.

## Adding New Content

### New Artwork:
1. Create new markdown file in appropriate category/year directory:
   `content/catalog-raisonne/painting/2024/new-artwork.md`

2. Front matter format:
   ```toml
   +++
   title = "Artwork Title"
   date = 2024-01-15
   category = "painting"
   year = 2024
   image = "/images/2024/01/artwork.jpg"
   image_alt = "Description of the artwork"
   +++
   
   Artwork description goes here.
   ```

3. Add image to `static/images/YYYY/MM/`

### New Pages:
Create markdown files in `content/` with proper template reference.

## Deployment

The `public/` directory contains the complete static site ready for deployment to any static hosting service.

- **Netlify**: Connect to this repository
- **GitHub Pages**: Deploy from `main` branch  
- **Vercel**: Import repository
- **Traditional hosting**: Upload `public/` contents

## Migration Notes

### What was preserved:
- All artwork content and metadata
- Artist statement and biography
- Site structure and navigation
- Social media links
- URL structure (with redirects setup)

### What was improved:
- Faster loading times
- Better mobile experience  
- Easier content management
- No database dependencies
- Future-proof file formats

### Next Steps:
1. Download original images from Ghost site
2. Add them to `static/images/` with proper organization
3. Update any remaining content as needed
4. Configure domain and hosting
5. Set up redirects from old URLs if necessary

## Customization

- Edit `sass/style.scss` for styling changes
- Modify `templates/` for layout changes
- Update `config.toml` for site configuration
- Content managed in `content/` markdown files

## Support

This implementation prioritizes:
- **Long-term maintainability** (no breaking dependencies)
- **Performance** (minimal, optimized code)
- **Accessibility** (semantic HTML, proper contrast)
- **Simplicity** (easy to understand and modify)