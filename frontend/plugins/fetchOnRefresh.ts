import Vue from 'vue'

/**
 * 在页面刷新后，恢复登录并执行当前页面的 fetch
 */
Vue.mixin({
    async beforeMount() {
        // @ts-ignore
        if (typeof this.$options.fetch == "function") {
            if (localStorage.token) {
                // @ts-ignore
                await this.$root.$options.context.store.dispatch("student/restoreLogin", {token: localStorage.token});
            }
            // @ts-ignore
            const data = await this.$options.fetch(this.$root.$options.context);

            for (let k in data) {
                // @ts-ignore
                this[k] = data[k];
            }
        }
    }
});