# DEPLOYMENT.md

## Summary
This guide shows how to deploy this Python project to **Render** using their Free plan (recommended for Python/Flask/Django hobby apps). Render supports free web services and provides GitHub integration so your repo auto-deploys on push.

## Files added
- `Dockerfile` - production Dockerfile using Gunicorn.
- `Procfile` - (optional) for some platforms.
- `render.yaml` - Render service spec (free plan).
- `.github/workflows/render-deploy.yml` - CI workflow to run tests on push.

## Assumptions
- Your app entrypoint is `app.py` with a Flask `app` object (change `app:app` in start commands if different).
- You have a `requirements.txt` at project root. If not, generate one: `pip freeze > requirements.txt`.
- You use Gunicorn for production. For Django, change the start command accordingly (e.g., `gunicorn myproject.wsgi:application`).

## Steps (quick)
1. Create a GitHub repo and push your project to `main`.
   ```
   git init
   git add .
   git commit -m "initial"
   git branch -M main
   git remote add origin git@github.com:<your-org>/<repo>.git
   git push -u origin main
   ```

2. Sign up / log in to Render (https://render.com) and choose **New -> Web Service**.
   - Connect your GitHub repo.
   - Select the branch `main`.
   - For Environment choose **Python**.
   - For Instance Type choose **Free**.
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`
   - If you used Dockerfile, Render will detect and build the Docker image automatically if you select Docker option.

3. Add environment variables in the Render dashboard under the service’s settings (e.g., `SECRET_KEY`, `DATABASE_URL`).

4. Visit the provided Render URL (staging) once deploy finishes. For production, add a custom domain if needed.

## If your app is a Django app
- Make sure `ALLOWED_HOSTS` includes `*` or your Render domain.
- Use `gunicorn myproject.wsgi:application` as the start command.
- Run database migrations in Render console if you use an attached database.

## Alternative free options
- Vercel supports Python serverless functions (limited), best for serverless endpoints.
- PythonAnywhere can host small Flask apps (upload or Git).
- Fly.io has changed its free tier; check current status before using.

## Rollback & Monitoring
- Render shows recent deploys and allows rollbacks to previous deploys.
- Use Render logs to debug; integrate Sentry for error tracking.

## Notes
- Free tiers have limits (sleeping instances, limited CPU, bandwidth). Don't use for critical production.
- If your project needs a database, Render offers free Postgres (with limits); alternatively use free-tier managed DBs (careful with limits).

