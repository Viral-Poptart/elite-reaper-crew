# Elite Reaper Crew status poster

Tracks Sadistichronic [2047491] via Torn's read-only API and publishes `status.png` through GitHub Pages.

## Setup
1. Upload `status.py`, `.github/workflows/update-status.yml`, and optionally your full-resolution poster as `poster.png` to the repository root. Without `poster.png`, the script creates a simple test badge.
2. In GitHub: Settings → Secrets and variables → Actions → New repository secret. Name: `TORN_API_KEY`. Value: a Torn API key with permission to read the target player's profile. Never commit it.
3. In GitHub: Settings → Actions → General → Workflow permissions, select **Read and write permissions**.
4. In Actions, run **Update faction status image** manually once.
5. In Settings → Pages, choose **Deploy from a branch**, branch `gh-pages`, folder `/ (root)`.
6. The public image URL should be `https://viral-poptart.github.io/elite-reaper-crew/status.png` after deployment.
7. Embed the image on Torn only if Torn permits externally hosted images. Test refreshing after a status change; Torn may cache images.

GitHub Actions scheduled runs may be delayed. `UNKNOWN` means API data could not be verified; it does not mean offline.

### Poster positioning
`status.py` assumes a **1024×1536** poster and places the badge inside THE COMMAND area at approximately x=695, y=1105. Adjust these coordinates for your exact poster. It overlays an existing area, so use a poster with enough empty space in that location.
