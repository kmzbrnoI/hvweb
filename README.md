# Public webpage with list of engines in hJOPserver

## Deployment

 1. `$ git clone --recurse-submodules https://github.com/kmzbrnoI/hvweb`
 2. Optional: setup virtualenv.
 3. Install Python packages from `requirements.txt`.
 4. Add directory with engines to `lok`.
    - The directory is usually a symlink to `lok` subfolder of `hJOPserverConfig`
      repository. The repository is either somewhere else in your filesystem or
      you can clone it to `hvsrepo` directory in this repository (this folder
      is gitignored). This is suitable for deployment.
 5. `$ make all`
 6. Serve webserver in `build` directory.
 7. Remake when database changes.

### Github autodeploy on push

 * Add deploy token to `build/deploy-token.php`.
