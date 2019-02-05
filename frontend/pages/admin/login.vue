<template>
    <v-card class="elevation-8">
        <v-card-text>
            <v-form>
                <v-text-field @keyup.enter="login" label="Admin Token" name="token" prepend-icon="person"
                              type="text" v-model="token"></v-text-field>
            </v-form>
        </v-card-text>
        <v-card-actions>
            <v-btn :disabled="loading" :loading="loading" @click="login" block color="primary">登录</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import Vue from 'vue';
    import * as adminModule from '~/store/modules/admin';

    const AdminNamespace = namespace(adminModule.name);
    @Component
    export default class Login extends Vue {
        @AdminNamespace.Action checkToken!: (payload: { token: string }) => Promise<boolean>;

        layout() {
            return "middleBox"
        }

        token: string = "";
        loading = false;

        async login() {
            this.loading = true;
            let result = await this.checkToken({token: this.token});
            if (result) {
                this.$router.push('/admin');
            } else {
                this.token = "";
            }
            this.loading = false;
        }
    }
</script>

<style scoped>

</style>