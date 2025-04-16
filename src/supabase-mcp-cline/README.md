# Wallpaper Generator

A web application for generating custom desktop wallpapers with various styles and effects, built with HTML, CSS, JavaScript, and Supabase.

## Features

- Generate wallpapers in multiple styles:
  - Gradient
  - Geometric
  - Particles (animated)
  - Waves
  - AI-Generated (using GPT-4o)
- Customize wallpaper settings:
  - Resolution (1080p, 2K, 4K, or custom)
  - Colors (dual colors or random)
  - Opacity
  - Blur effects
  - Text prompts for AI-generated wallpapers
- Save wallpapers to your personal gallery
- Download wallpapers as PNG files
- User authentication via Supabase
- Responsive design for desktop and mobile

## Demo

To see a demo of the application, open the `public/demo.html` file in your browser.

## Setup Instructions

### Prerequisites

- [Supabase Account](https://supabase.com/)
- [OpenAI API Key](https://platform.openai.com/api-keys) (for AI-generated wallpapers)
- Web browser

### Local Development

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/wallpaper-generator.git
   cd wallpaper-generator
   ```

2. Open `index.html` in your browser to use the application locally.

### Supabase Setup

1. Create a new Supabase project at [https://app.supabase.com](https://app.supabase.com)

2. Get your Supabase URL and anon key from the project settings.

3. Update the Supabase configuration in `js/config.js`:
   ```javascript
   const SUPABASE_CONFIG = {
       url: 'YOUR_SUPABASE_URL',
       anonKey: 'YOUR_SUPABASE_ANON_KEY'
   };
   ```

4. Apply the database migration:
   - Go to the SQL Editor in your Supabase dashboard
   - Copy the contents of `migrations/001_initial_schema.sql`
   - Paste and run the SQL in the editor

5. Enable Email Auth in Authentication settings.

### Supabase Edge Function Setup

1. Create an account at [OpenAI](https://platform.openai.com/) if you don't have one.

2. Generate an API key in the [API Keys section](https://platform.openai.com/api-keys).

3. Install the Supabase CLI if you haven't already:
   ```bash
   npm install -g supabase
   ```

4. Login to Supabase CLI:
   ```bash
   supabase login
   ```

5. **Option 1: Use the deployment script (recommended)**
   
   Run the provided deployment script:
   ```bash
   ./supabase/functions/deploy.sh
   ```
   
   The script will:
   - Check if Supabase CLI is installed and you're logged in
   - Link your project
   - Deploy the Edge Function
   - Prompt you for your OpenAI API key and set it as a secret

6. **Option 2: Manual deployment**
   
   Link your project:
   ```bash
   supabase link --project-ref mtrdeegsedalhmrmqdwl
   ```

   Deploy the Edge Function:
   ```bash
   supabase functions deploy generate-image --no-verify-jwt
   ```

   Set the OpenAI API key as a secret:
   ```bash
   supabase secrets set OPENAI_API_KEY=YOUR_OPENAI_API_KEY
   ```

## How to Use

1. Open the application in your web browser.

2. Select your desired wallpaper style, resolution, and colors.
   - For AI-generated wallpapers, select "AI Generated" from the style dropdown and enter a descriptive prompt.

3. Click "Generate Wallpaper" to create a new wallpaper (or "Generate with AI" for AI-generated wallpapers).

4. Adjust settings as needed to customize your wallpaper.

5. Click "Download" to save the wallpaper to your device.

6. To save wallpapers to your gallery:
   - Sign in or create an account
   - Click "Save to Gallery"
   - Access your saved wallpapers in the gallery section

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Supabase (Authentication, Database, Storage)
- **AI Image Generation**: OpenAI GPT-4o API
- **Graphics**: HTML5 Canvas API
- **Styling**: Custom CSS

## Project Structure

```
wallpaper-generator/
├── index.html          # Main HTML file
├── css/
│   └── styles.css      # Stylesheet
├── js/
│   ├── app.js          # Application logic
│   ├── config.js       # Supabase configuration
│   └── openai-config.js # OpenAI configuration
├── migrations/
│   └── 001_initial_schema.sql  # Database schema
├── public/             # Public assets
│   └── demo.html       # Demo page
├── supabase/
│   └── functions/
│       ├── _shared/
│       │   └── cors.ts # Shared CORS headers
│       ├── generate-image/
│       │   └── index.ts # AI image generation Edge Function
│       ├── deno.json    # Deno configuration
│       ├── .gitignore   # Git ignore for functions
│       └── deploy.sh    # Deployment script
└── README.md           # Documentation
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
