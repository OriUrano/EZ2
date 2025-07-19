# EZ2 Project - Claude Instructions

## Project Overview
EZ2 is an EC2 dashboard built with SvelteKit and Tailwind CSS that displays AWS EC2 instance information via a serverless Lambda backend.

## Technology Stack
- **Frontend**: SvelteKit 2.x with Svelte 5.x
- **Styling**: Tailwind CSS 4.x
- **Backend**: AWS Lambda (Python 3.9) with Function URLs
- **Testing**: Vitest + Playwright
- **Build**: Vite 7.x

## Development Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run unit and e2e tests
- `npm run format` - Format code with Prettier
- `npm run lint` - Lint code with Prettier
- `npm run check` - Type check with svelte-check

## Project Structure
```
src/
├── routes/
│   ├── +layout.svelte          # Main layout with navigation
│   ├── +page.svelte            # Home page (dashboard)
│   └── dashboard/
│       └── +page.svelte        # EC2 dashboard page
├── lib/
│   └── index.ts               # Shared utilities
├── app.css                    # Global styles
├── app.d.ts                   # TypeScript declarations
└── app.html                   # HTML template

lambda/
├── ec2_handler.py             # Lambda function for EC2 API
└── requirements.txt           # Python dependencies
```

## Key Features
1. **EC2 Instance Monitoring** - Real-time display of EC2 instances with status, IP addresses, instance types, and metadata
2. **Responsive Design** - Mobile-friendly interface using Tailwind CSS
3. **Serverless Backend** - Lambda Function URLs for API endpoints
4. **Static Site Generation** - Can be deployed as static site

## Important Notes
- Uses Svelte 5 syntax with `$state()` for reactivity
- Lambda Function URL must be configured in the dashboard UI
- Requires specific IAM permissions for Lambda to access EC2
- Static site generation enabled for deployment flexibility

## Coding Standards
- Use Tailwind CSS classes for styling
- Follow Svelte 5 best practices
- Maintain responsive design patterns
- Keep components focused and reusable
- Use TypeScript for type safety