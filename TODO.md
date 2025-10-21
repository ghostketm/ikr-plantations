# TODO: Configure Render Free Tier Deployment

## Tasks
- [x] Update render.yaml to specify "plan: free" for web service and database
- [x] Update RENDER_DEPLOYMENT_GUIDE.md with free tier limitations and setup details
- [x] Verify render.yaml syntax and compatibility with free tier limitations
- [x] Test basic functionality locally (development server runs, pages load with 200 status)

## Notes
- Free web services spin down after 15 minutes of inactivity
- Free PostgreSQL has 1GB limit and expires after 30 days
- Ensure app handles spinning down gracefully (no persistent state)
- Local testing passed: server starts, home/listings/agents pages return 200
