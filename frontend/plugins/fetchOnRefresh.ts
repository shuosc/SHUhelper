import Vue from 'vue'

Vue.mixin({
    async beforeMount() {
        // @ts-ignore
        if (typeof this.$root.$options.context.from == 'undefined'
            // @ts-ignore
            && this.$router.history.current.path != '/'
            // @ts-ignore
            && typeof this.$options.fetch == "function") {

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