# A rule that:

# 1. Queries to find all doc_publish targets in the repo
# bazel query 'kind("doc_publish rule", //...)'
# 2. Calls them all
# 3. Grabs their artefacts and preprocesses them as required for Jekyll

def doc_site_stage(ctx, build_mode):