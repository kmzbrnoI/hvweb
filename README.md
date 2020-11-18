# Public webpage with list of engines in hJOPserver

## Deployment

 1. `$ git clone --recurse-submodules https://github.com/kmzbrnoI/hvweb`
 2. Add directory with engines to `lok`.
 3. `$ mase all`
 4. Serve webserver in `build` directory.
 5. Remake when database changed.

## Github autodeploy on push

 * Add deploy token to `build/deploy-token.php`.
