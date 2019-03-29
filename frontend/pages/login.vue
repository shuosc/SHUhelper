<template>
    <v-card class="elevation-8">
        <v-card-text>
            <v-form>
                <v-text-field v-model="username" prepend-icon="person" name="username" label="一卡通账号"
                              @keyup.enter="doLogin" type="text"></v-text-field>
                <v-text-field v-model="password" prepend-icon="lock" name="password" label="密码"
                              @keyup.enter="doLogin" type="password"></v-text-field>
                <v-dialog v-model="errorLogin" width="500">
                    <v-card>
                        <v-card-text>
                            学号或密码错误，请重试
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions>
                            <v-btn @click="errorLogin = false " block color="primary">
                                确定
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-form>
        </v-card-text>
        <v-card-actions>
            <v-btn :loading="loading" :disabled="loading" @click="doLogin" block color="primary">登录</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script lang="ts">
    import {namespace} from "vuex-class";
    import {Option} from "fp-ts/lib/Option";
    import {Student} from "../../shared/model/student/student";
    import {Component, Vue} from "vue-property-decorator";

    const StudentNamespace = namespace("student");
    @Component({
        layout: "middleBox"
    })
    export default class Login extends Vue {
        username: string = "";
        password: string = "";
        loading = false;
        errorLogin = false;

        @StudentNamespace.Getter student!: Option<Student>;
        @StudentNamespace.Getter token!: string;
        @StudentNamespace.Action login!: (payload: { username: string, password: string }) => void;

        async doLogin() {
            this.loading = true;
            try {
                await this.login({username: this.username, password: this.password});
            } catch (e) {
                this.errorLogin = true
            }
            if (this.student.isSome()) {
                this.$router.push('/');
                localStorage.token = this.token;
            }
        }
    }
</script>

<style scoped>

</style>
