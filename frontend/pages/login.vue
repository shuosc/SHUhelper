<template>
    <v-card class="elevation-8">
        <v-card-text>
            <v-form>
                <v-text-field v-model="username" prepend-icon="person" name="username" label="一卡通账号"
                              @keyup.enter="login" type="text"></v-text-field>
                <v-text-field v-model="password" prepend-icon="lock" name="password" label="密码"
                              @keyup.enter="login" type="password"></v-text-field>
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
    import * as studentModule from '~/store/modules/student';
    import {Student} from '~/store/modules/student';
    import {Maybe} from "../../shared/tools/functools/maybe";

    const StudentNamespace = namespace(studentModule.name);
    @Component
    export default class Login extends Vue {
        layout() {
            return "middleBox"
        }

        username: string = "";
        password: string = "";
        loading = false;

        @StudentNamespace.Action doLogin!: (payload: { username: string, password: string }) => Promise<void>;
        @StudentNamespace.Getter student!: Maybe<Student>;


        async login() {
            this.loading = true;
            await this.doLogin({username: this.username, password: this.password});
            if (this.student.value !== null) {
                this.$router.push('/');
                localStorage.token = this.student.value.token;
            }
        }
    }
</script>

<style scoped>

</style>