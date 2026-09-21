#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>

#include <openssl/crypto.h>

/*
 * CTF-only support module.  The secret is copied repeatedly to allocations
 * made by OpenSSL itself, making the otherwise non-deterministic disclosure
 * observable during a local exercise.  No request handler exposes this data.
 */
static ngx_int_t ngx_http_heartbleed_flag_init_process(ngx_cycle_t *cycle);
static char *ngx_http_heartbleed_flag_seed(ngx_conf_t *cf, ngx_command_t *cmd,
    void *conf);

static ngx_command_t ngx_http_heartbleed_flag_commands[] = {
    {
        ngx_string("heartbleed_flag_seed"),
        NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_CONF_FLAG,
        ngx_http_heartbleed_flag_seed,
        0,
        0,
        NULL
    },
    ngx_null_command
};

static ngx_http_module_t ngx_http_heartbleed_flag_module_ctx = {
    NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
};

ngx_module_t ngx_http_heartbleed_flag_module = {
    NGX_MODULE_V1,
    &ngx_http_heartbleed_flag_module_ctx,
    ngx_http_heartbleed_flag_commands,
    NGX_HTTP_MODULE,
    NULL, NULL, ngx_http_heartbleed_flag_init_process, NULL, NULL, NULL, NULL,
    NGX_MODULE_V1_PADDING
};

static char *
ngx_http_heartbleed_flag_seed(ngx_conf_t *cf, ngx_command_t *cmd, void *conf)
{
    ngx_str_t *value = cf->args->elts;

    if (value[1].len == 2 && ngx_strncmp(value[1].data, "on", 2) == 0) {
        return NGX_CONF_OK;
    }

    return "must be set to 'on'";
}

static ngx_int_t
ngx_http_heartbleed_flag_init_process(ngx_cycle_t *cycle)
{
    static const char flag[] = "flag{heartbeats_must_validate_their_length}";
    u_char *seed;
    ngx_uint_t i;

    for (i = 0; i < 128; i++) {
        seed = OPENSSL_malloc(4096);
        if (seed == NULL) {
            return NGX_ERROR;
        }
        ngx_memzero(seed, 4096);
        ngx_memcpy(seed, flag, sizeof(flag));
    }

    return NGX_OK;
}
