# Public webpage with list of engines in hJOPserver

## Deployment

 1. `$ git clone --recurse-submodules https://github.com/kmzbrnoI/hvweb`
 2. Install Python packages.
 3. Add directory with engines to `lok`.
 4. `$ mase all`
 5. Serve webserver in `build` directory.
 6. Remake when database changed.

## Github autodeploy on push

 * Add deploy token to `build/deploy-token.php`.
