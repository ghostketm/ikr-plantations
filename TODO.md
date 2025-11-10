# Fix Listing Images Not Rendering in Production

## Issue
Listing images are not being rendered in production after adding listings as admin. This is because Render uses ephemeral file storage, so uploaded media files are not persisted.

## Plan
1. Configure Cloudinary for cloud storage of media files
2. Add Cloudinary dependencies
3. Update settings for cloud storage
4. Add environment variables to render.yaml
5. Fix ListingForm to handle image uploads
6. Update listing creation view to save images

## Steps
- [x] Add cloudinary and django-cloudinary-storage to requirements.txt
- [x] Configure CLOUDINARY_STORAGE in production settings
- [x] Add Cloudinary env vars to render.yaml
- [x] Add images field to ListingForm
- [x] Update listing_create view to handle image saving
- [ ] Test image upload and rendering in production
