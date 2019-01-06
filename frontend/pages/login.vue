<template>
    <v-card class="elevation-8">
        <v-card-text>
            <v-form>
                <v-text-field v-model="username" prepend-icon="person" name="username" label="一卡通账号"
                              type="text"></v-text-field>
                <v-text-field v-model="password" prepend-icon="lock" name="password" label="密码"
                              type="password"></v-text-field>
            </v-form>
        </v-card-text>
        <v-card-actions>
            <v-btn :loading="loading" :disabled="loading" @click="login" block color="primary">登录</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import Vue from 'vue';
    import * as student from '~/store/modules/student';

    const Student = namespace(student.name);
    @Component
    export default class Login extends Vue {
        layout() {
            return "middleBox"
        }

        username: string = "";
        password: string = "";
        @Student.Action doLogin: any;
        @Student.Getter isLogged: any;
        loading = false;

        async login() {
            this.loading = true;
            await this.doLogin({username: this.username, password: this.password});
            this.$router.push('/');
        }
    }
</script>

<style scoped>

</style>