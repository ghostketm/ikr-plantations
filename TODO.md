# TODO: Fix Media Rendering and Agent Listing Issues

## 1. Configure Cloudinary for Media Storage
- [x] Update `ikr_project/settings/production.py` to ensure Cloudinary is properly configured for media files
- [ ] Guide user to set up Cloudinary environment variables in Render dashboard (CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_URL)

## 2. Modify Agent List to Show All Agents
- [x] Update `apps/agents/views.py` to show all AgentProfile objects ordered by verification_status ascending
- [x] Update `templates/agents/agent_list.html` to indicate verification status (e.g., add a badge for unverified agents)

## 3. Followup Steps
- [ ] Set Cloudinary env vars in Render dashboard
- [ ] Test media uploads and rendering in production
- [ ] Verify agent list shows all agents (verified first)
