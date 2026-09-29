# LabLend Demo: Step-by-Step Guide for Windows

Follow the steps **in order**. Each step has one job. Do not skip ahead until you see the result described under **✅ You should see**.

**You need:** a Windows 10/11 laptop with at least 8 GB RAM, internet, a GitHub account, and the file **`lablend-demo.zip`** (downloaded from our chat).

**You will type all commands in PowerShell.** To open it: press the **Windows key**, type `PowerShell`, press **Enter**. To paste a command into PowerShell, **right-click** inside the window.

| Part | What you do | Time |
|---|---|---|
| A | Install the tools | 45 min |
| B | Put the project on your laptop and GitHub | 15 min |
| C | Run the app with Docker | 15 min |
| D | Install Jenkins | 30 min |
| E | Create the pipeline | 20 min |
| F | Prove automatic deployment | 10 min |
| G | Prove failed-test blocking and rollback | 15 min |
| H | Classroom demo checklist | — |

---

## PART A: Install the tools

### Step 1. Turn on WSL 2

1. Press the **Windows key**, type `PowerShell`, **right-click** "Windows PowerShell", choose **Run as administrator**.
2. Type:
   ```powershell
   wsl --install
   ```
3. When it finishes, **restart your laptop**.

✅ **You should see:** after restarting, an Ubuntu window may open and ask for a username and password. Create any username and password and close the window.

### Step 2. Install Docker Desktop

1. Go to **https://www.docker.com/products/docker-desktop/** and download **Docker Desktop for Windows**.
2. Run the installer. Keep **"Use WSL 2 instead of Hyper-V"** checked. Click **OK**, then **Close and restart** if asked.
3. Open **Docker Desktop** from the Start menu. Accept the agreement. You can skip sign-in.
4. Wait until the bottom-left corner says **Engine running** (green).

✅ **You should see:** "Engine running" in Docker Desktop.

### Step 3. Install Git

1. Go to **https://git-scm.com/download/win** and download Git for Windows.
2. Run the installer and click **Next** on every screen (the defaults are fine).

### Step 4. Check that everything works

Open a **new** PowerShell window (normal, not administrator) and run these one at a time:

```powershell
docker version
docker compose version
git --version
docker run hello-world
```

✅ **You should see:** version numbers for the first three, and **"Hello from Docker!"** for the last one.

### Step 5. Tell Git your name

```powershell
git config --global user.name "Frances Mendoza"
git config --global user.email "your-email@example.com"
```

(Use the email address of your GitHub account.)

---

## PART B: Put the project on your laptop and on GitHub

### Step 6. Unzip the project into Documents

In PowerShell:

```powershell
Expand-Archive "$HOME\Downloads\lablend-demo.zip" -DestinationPath "$HOME\Documents"
cd "$HOME\Documents\lablend-demo"
dir
```

✅ **You should see:** folders `borrow-api`, `db`, `docs`, `frontend`, `infra`, `items-api`, `proxy`, and files `docker-compose.yml`, `Jenkinsfile`, `README.md`.

> If your zip is not in Downloads, change the path in the first command.

### Step 7. Create an empty repository on GitHub

1. Go to **https://github.com/new**.
2. Repository name: `lablend-demo`
3. Choose **Public**.
4. **Do NOT** tick "Add a README" (leave everything unticked).
5. Click **Create repository**.
6. Keep this page open. You need the URL shown there, which looks like
   `https://github.com/YOUR-USERNAME/lablend-demo.git`

### Step 8. Upload the project to GitHub

In PowerShell (still inside the `lablend-demo` folder), run one line at a time. Replace `YOUR-USERNAME` with your GitHub username:

```powershell
git init -b main
git add .
git commit -m "Initial LabLend project"
git remote add origin https://github.com/YOUR-USERNAME/lablend-demo.git
git push -u origin main
```

A window will pop up asking you to sign in to GitHub. Choose **Sign in with your browser** and approve.

✅ **You should see:** refresh the GitHub page. All the project folders are now there.

---

## PART C: Run the app with Docker

### Step 9. Create your password file (`.env`)

```powershell
Copy-Item .env.example .env
notepad .env
```

Notepad opens. Change the last line from `DB_PASSWORD=change-me` to your own password, for example:

```
DB_NAME=lablend
DB_USER=lablend
DB_PASSWORD=LabLend2026
```

Click **File → Save**, then close Notepad.

> ⚠️ **Write this password down.** You will give the same file to Jenkins in Step 20. This `.env` file is never uploaded to GitHub (the `.gitignore` file blocks it).

### Step 10. Start the whole app

```powershell
docker compose up -d --build
```

The first time takes 5 to 10 minutes because it downloads images.

✅ **You should see:** lines ending with `Started` or `Healthy` for `lablend-db-1`, `lablend-items-api-1`, `lablend-borrow-api-1`, `lablend-frontend-1`, and `lablend-proxy-1`.

### Step 11. Check that all containers are healthy

```powershell
docker compose ps
```

✅ **You should see:** 5 containers, and the STATUS column says `(healthy)` for db, items-api, borrow-api, and frontend. If it says `(health: starting)`, wait 30 seconds and run it again.

### Step 12. Open the app

Open your browser and go to **http://localhost:8080**

✅ **You should see:** the LabLend page with 4 equipment items, and **Build dev** at the bottom.

Try it: add one equipment item, borrow one item, and return it.

### Step 13. Prove the data is saved (persistence)

```powershell
docker compose down
docker compose up -d
```

> ⚠️ Never add `-v` to `docker compose down`. `-v` deletes the database.

Refresh the browser.

✅ **You should see:** the item and borrow record you created in Step 12 are still there.

---

## PART D: Install Jenkins

### Step 14. Start Jenkins

```powershell
cd infra\jenkins
docker compose up -d --build
cd ..\..
```

The first time takes 5 to 10 minutes.

✅ **You should see:** `Container jenkins Started`.

### Step 15. Get the Jenkins unlock password

```powershell
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

✅ **You should see:** a long code such as `3f9a8c...`. Copy it (select it and press **Enter**, or right-click → Copy).

> If you get an error, wait 1 minute (Jenkins is still starting) and try again.

### Step 16. Unlock Jenkins

1. Open **http://localhost:8081**
2. Paste the code into **Administrator password**. Click **Continue**.
3. Click **Install suggested plugins**. Wait until all items are green (about 5 minutes).

### Step 17. Create your Jenkins admin account

1. Fill in username (e.g. `admin`), password, full name, email.
2. Click **Save and Continue** → **Save and Finish** → **Start using Jenkins**.

✅ **You should see:** the Jenkins dashboard ("Welcome to Jenkins!").

### Step 18. Install two extra plugins

1. Click **Manage Jenkins** (left side) → **Plugins** → **Available plugins**.
2. In the search box type `Docker Pipeline` and tick it.
3. Clear the search box, type `Stage View`, and tick **Pipeline: Stage View**. (If it does not appear, it is already installed. That is fine.)
4. Click **Install**.
5. At the bottom, tick **Restart Jenkins when installation is complete and no jobs are running**.
6. Wait 1 minute, then log in again.

### Step 19. Check that Jenkins can control Docker

In PowerShell:

```powershell
docker exec jenkins docker ps
```

✅ **You should see:** a list that includes your `lablend-...` containers and `jenkins`.

### Step 20. Give Jenkins your password file

1. In Jenkins click **Manage Jenkins** → **Credentials**.
2. Click **(global)** (under "Domains") → **Add Credentials** (top right).
3. **Kind:** choose **Secret file**.
4. **File:** click **Choose File**, go to `Documents\lablend-demo`, and select **`.env`** (the one you edited in Step 9, *not* `.env.example`).
5. **ID:** type exactly `lablend-env`
6. **Description:** `LabLend .env`
7. Click **Create**.

✅ **You should see:** `lablend-env` listed under Credentials.

---

## PART E: Create the pipeline

### Step 21. Create a Pipeline job

1. Go back to the Jenkins dashboard (click the **Jenkins** logo, top left).
2. Click **New Item**.
3. Name: `lablend`
4. Click **Pipeline**, then click **OK**.

### Step 22. Connect the job to GitHub

On the configuration page, scroll all the way down to the **Pipeline** section:

1. **Definition:** choose **Pipeline script from SCM**
2. **SCM:** choose **Git**
3. **Repository URL:** `https://github.com/YOUR-USERNAME/lablend-demo.git`
4. **Credentials:** leave as `- none -`
5. **Branch Specifier:** change `*/master` to **`*/main`** ⚠️ (very important)
6. **Script Path:** leave as `Jenkinsfile`
7. Do not tick anything under "Triggers". Click **Save**.

### Step 23. Run the first build by hand (only this once)

Click **Build Now** (left side).

> This one manual build is required. Jenkins reads the `Jenkinsfile` during this build and learns that it should check GitHub every minute. **After this, you never press Build Now again.**

### Step 24. Watch the build

1. Under **Builds** (bottom left), click **#1**.
2. Click **Console Output**.
3. Wait. The first build takes 5 to 10 minutes.

✅ **You should see:** at the end, **`Smoke test passed: build 1 is live`** and **`Finished: SUCCESS`**.

### Step 25. Check the Stage View

Click **lablend** at the top to go back to the job page.

✅ **You should see:** five green boxes: **Checkout, Test, Build Images, Deploy, Smoke Test**.

### Step 26. Check the app

Refresh **http://localhost:8080**

✅ **You should see:** the footer now says **Build 1**, and your old records from Step 12 are still there.

---

## PART F: Prove automatic deployment

### Step 27. Make a visible change

In PowerShell (inside `Documents\lablend-demo`):

```powershell
notepad frontend\index.html
```

Find this line (press **Ctrl + F** and search `<h1>`):

```html
<h1>LabLend: Lab Equipment Borrowing</h1>
```

Change it to:

```html
<h1>LabLend: Now with Auto-Deploy!</h1>
```

Save and close Notepad.

### Step 28. Push the change

```powershell
git add .
git commit -m "Change heading"
git push
```

### Step 29. Watch Jenkins start by itself

**Do not click anything in Jenkins.** Open the `lablend` job page and wait up to 1 minute.

✅ **You should see:** build **#2** appears by itself. Click it → **Console Output**. The first line says **"Started by an SCM change"**. This is your proof that the push triggered it, not a person.

### Step 30. Check the result

When build #2 finishes, go to **http://localhost:8080** and press **Ctrl + F5**.

✅ **You should see:** the new heading and **Build 2** in the footer.

---

## PART G: Prove failed-test blocking and rollback

### Step 31. Break a rule on purpose

```powershell
notepad borrow-api\logic.py
```

Find:

```python
LOAN_DAYS = 3  # equipment must be returned within 3 days
```

Change the `3` to `5`:

```python
LOAN_DAYS = 5  # equipment must be returned within 3 days
```

Save and close.

### Step 32. Push the broken code

```powershell
git commit -am "Change loan period to 5 days"
git push
```

### Step 33. Watch the pipeline stop

Wait for build **#3** to start by itself.

✅ **You should see:**
- The **Test** box is **red**. Build Images, Deploy, and Smoke Test do not run.
- In Console Output: **`2 failed`** (the tests expected a 3-day loan).
- **http://localhost:8080** still shows **Build 2**. The broken code never went live.

### Step 34. Fix it by undoing the commit

```powershell
git revert --no-edit HEAD
git push
```

✅ **You should see:** build **#4** starts by itself, all stages green, and the footer says **Build 4**.

### Step 35. Roll back to an older version

First, see which versions exist:

```powershell
docker images lablend/frontend
```

✅ **You should see:** tags `1`, `2`, `4`, and `dev`.

Now roll back to Build 1:

```powershell
$env:TAG = "1"
docker compose up -d --no-build
Remove-Item Env:TAG
```

Refresh the browser with **Ctrl + F5**.

✅ **You should see:** **Build 1** and the old heading, and your records are still there.

> The last line (`Remove-Item Env:TAG`) clears the setting so later commands are not stuck on Build 1.

### Step 36. Go back to the newest version

Push any small change (Steps 27 and 28) or run the rollback command again with the newest number, e.g. `$env:TAG = "4"`.

🎉 **Done.** You now have everything required by the project guidelines working on your laptop.

---

## PART H: Classroom demo checklist

**Before class (10 minutes early):**

1. Open **Docker Desktop** and wait for "Engine running". Your app and Jenkins start automatically (they are set to `restart: unless-stopped`).
2. Open **http://localhost:8080** (app) and **http://localhost:8081** (Jenkins) in two browser tabs.
3. Open PowerShell and run `cd "$HOME\Documents\lablend-demo"`.
4. Have a backup screen recording of Parts F and G in case the internet fails.

**During the demo, do these in order:**

| # | Action | Steps |
|---|---|---|
| 1 | Show running containers (`docker compose ps`) and the app with its build number | 11, 12 |
| 2 | Change the heading and push | 27, 28 |
| 3 | Show Jenkins starting by itself ("Started by an SCM change") and explain each stage | 29 |
| 4 | Show the new heading and build number | 30 |
| 5 | Push broken code; show red Test stage and the unchanged app | 31 to 33 |
| 6 | Revert and push; show it goes green | 34 |
| 7 | Show data is still there after all these deployments | 26 |
| 8 | Roll back to an older build | 35 |
| 9 | Explain the security note (below) | — |

**Security note to explain:** Jenkins runs as `root` and has access to Docker (`/var/run/docker.sock`), so it controls every container on the laptop. That is acceptable for a lab, but not in real production. Safer options: separate build agents, rootless Docker, Docker-in-Docker with TLS, or Kaniko.

---

## If something goes wrong

| Problem | Fix |
|---|---|
| Docker Desktop says WSL or virtualization error | Restart the laptop. If it persists, enable **Virtualization** in the BIOS (search your laptop model + "enable virtualization"). |
| `docker compose up` says **port is already allocated** | Another program uses port 8080. Open `docker-compose.yml` in Notepad, change `"8080:80"` to `"8088:80"`, and use http://localhost:8088 |
| Browser shows **502 Bad Gateway** | Wait 30 seconds and refresh. If it stays, run `docker compose ps` and `docker compose logs items-api` |
| Jenkins build fails at **Checkout** | Check the Repository URL (Step 22) and that the Branch Specifier is `*/main` |
| Jenkins says **Could not find credentials entry with ID 'lablend-env'** | Redo Step 20; the ID must be exactly `lablend-env` |
| Jenkins says **permission denied ... docker.sock** | In PowerShell: `cd infra\jenkins`, `docker compose up -d --force-recreate`, `cd ..\..` |
| Logs show **password authentication failed** | The `.env` in Jenkins has a different password from Step 9. Upload the same `.env` again (Step 20, click the credential → **Update**). |
| Pushing does not start a build | Make sure you did Step 23 (the one manual build). In the job, click **Git Polling Log** to see what Jenkins checked. |
| Page still shows the old build number | Press **Ctrl + F5** |
| You want to start completely fresh (**deletes all data**) | `docker compose down -v`, then go back to Step 10 |

---

## Appendix: What each folder does (for explaining to students)

| Folder / file | Purpose |
|---|---|
| `db/` | PostgreSQL image with `init.sql` (creates tables and 4 sample items) |
| `items-api/` | Python Flask service: list and add equipment. Tests in `tests/` |
| `borrow-api/` | Python Flask service: borrow and return; due date = 3 days. Tests in `tests/` |
| `frontend/` | The web page; the footer shows the Jenkins build number |
| `proxy/` | Nginx: the only entry point (port 8080). Sends `/api/items/` and `/api/borrows/` to the right service |
| `docker-compose.yml` | Starts all 5 app containers with one command; database stored in volume `db-data` |
| `.env.example` | Sample password file (the real `.env` is never uploaded) |
| `Jenkinsfile` | The pipeline: Checkout → Test → Build Images → Deploy → Smoke Test; checks GitHub every minute |
| `infra/jenkins/` | Jenkins in its own container, kept separate from the app |
| Each `Dockerfile` for the APIs | Has a **test** stage (runs pytest; Jenkins uses this) and a **production** stage (runs the app as a non-root user) |
