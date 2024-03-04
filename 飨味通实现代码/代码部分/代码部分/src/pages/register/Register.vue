<template>
  <common-layout>
    <div class="top">
      <div class="header">
        <img alt="logo" class="logo" src="@/assets/img/logo.png"/>
        <span class="title">{{ systemName }}</span>
      </div>
      <div class="desc">用户注册</div>
    </div>
    <div class="login">
      <a-form @submit="onSubmit" :form="form">
        <a-tabs size="large" :tabBarStyle="{textAlign: 'center'}" style="padding: 0 2px;">
          <a-tab-pane tab="账户密码注册" key="1">
            <a-alert type="error" :closable="true" v-if="error" :message="error" @close='onClose' showIcon
                     style="margin-bottom: 24px;"/>
            <a-form-item>
              <a-input
                  autocomplete="autocomplete"
                  size="large"
                  placeholder="用户名"
                  v-decorator="['name', {rules: [{ required: true, message: '请输入账户名', whitespace: true}]}]"
              >
                <a-icon slot="prefix" type="user"/>
              </a-input>
            </a-form-item>
            <a-form-item>
              <a-input
                  autocomplete="autocomplete"
                  size="large"
                  placeholder="手机号"
                  v-decorator="['mobile number', {rules: [{ required: true, message: '请输入手机号', whitespace: true}]}]"
              >
                <a-icon slot="prefix" type="mobile"/>
              </a-input>
            </a-form-item>
            <a-form-item>
              <a-input
                  size="large"
                  placeholder="密码"
                  autocomplete="autocomplete"
                  type="password"
                  v-decorator="['password', {rules: [{ required: true, message: '请输入密码', whitespace: true}]}]"
              >
                <a-icon slot="prefix" type="lock"/>
              </a-input>
            </a-form-item>
            <div>
              <router-link style="float: right" to="login" >已有账号?去登录</router-link>
            </div>
          </a-tab-pane>
<!--          <a-tab-pane tab="手机号注册" key="2">-->
<!--            <a-alert type="error" :closable="true" v-if="error" :message="error" @close='onClose' showIcon-->
<!--                     style="margin-bottom: 24px;"/>-->
<!--            <a-form-item>-->
<!--              <a-input-->
<!--                  autocomplete="autocomplete"-->
<!--                  size="large"-->
<!--                  placeholder="手机号"-->
<!--                  v-decorator="['mobile number', {rules: [{ required: true, message: '请输入手机号', whitespace: true}]}]"-->
<!--              >-->
<!--                <a-icon slot="prefix" type="mobile"/>-->
<!--              </a-input>-->
<!--            </a-form-item>-->
<!--            <a-form-item>-->
<!--              <a-input-->
<!--                  size="large"-->
<!--                  placeholder="密码"-->
<!--                  autocomplete="autocomplete"-->
<!--                  type="password"-->
<!--                  v-decorator="['password', {rules: [{ required: true, message: '请输入密码', whitespace: true}]}]"-->
<!--              >-->
<!--                <a-icon slot="prefix" type="lock"/>-->
<!--              </a-input>-->
<!--            </a-form-item>-->
<!--          </a-tab-pane>-->
        </a-tabs>
        <a-form-item>
          <a-button :loading="logging" style="width: 100%;margin-top: 24px" size="large" htmlType="submit"
                    type="primary" @click="sendNewUser()">注册
          </a-button>
        </a-form-item>
      </a-form>
    </div>
  </common-layout>
</template>

<script>
import CommonLayout from '@/layouts/CommonLayout'
import axios from "axios";
import {message} from "ant-design-vue";
// import {login, getRoutesConfig} from '@/services/user'
// import {setAuthorization} from '@/utils/request'
// import {loadRoutes} from '@/utils/routerUtil'
// import {mapMutations} from 'vuex'
// import {login} from "@/services/user";

export default {
  name: 'Login',
  components: {CommonLayout},
  data() {
    return {
      logging: false,
      error: '',
      form: this.$form.createForm(this)
    }
  },
  computed: {
    systemName() {
      return this.$store.state.setting.systemName
    }
  },
  methods: {
    // async register(name, password) {
    //   try {
    //     const request = {}
    //   }
    // },
    onSubmit(e) {
      e.preventDefault()
      this.form.validateFields((err) => {
        if (!err) {
          this.logging = true
          // const name = this.form.getFieldValue('name')
          // const password = this.form.getFieldValue('password')
          // register(name, password);
        }
      })
    },
    onClose() {
      this.error = false;
    },
    sendNewUser() {
      this.addNewUser({
          Uname: this.form.getFieldValue('name'),
          phone: this.form.getFieldValue('mobile number'),
          pwd: this.form.getFieldValue('password')
      })
      setTimeout( ()=>{
        this.$router.push('/login');
      }, 800)
    },
    async addNewUser(userInfo) {
      try {
        const response = await axios.post('AddUser/', userInfo);
        if (!response.data.value) {
          message.success(response.data.message)
        } else {
          message.error(response.data.message)
        }
      } catch (error) {
        console.error('Error fetching dish data:', error);
        message.error('Failed to fetch dish data.');
      }
    },
  }
}
</script>

<style lang="less" scoped>
.common-layout {
  .top {
    text-align: center;

    .header {
      height: 44px;
      line-height: 44px;

      a {
        text-decoration: none;
      }

      .logo {
        height: 44px;
        vertical-align: top;
        margin-right: 16px;
      }

      .title {
        font-size: 33px;
        color: @title-color;
        font-family: 'Myriad Pro', 'Helvetica Neue', Arial, Helvetica, sans-serif;
        font-weight: 600;
        position: relative;
        top: 2px;
      }
    }

    .desc {
      font-size: 20px;
      color: @text-color-second;
      margin-top: 12px;
      margin-bottom: 40px;
    }
  }

  .login {
    width: 368px;
    margin: 0 auto;
    @media screen and (max-width: 576px) {
      width: 95%;
    }
    //@media screen and (max-width: 320px) {
    //  .captcha-button{
    //    font-size: 14px;
    //  }
    //}
    .icon {
      font-size: 24px;
      color: @text-color-second;
      margin-left: 16px;
      vertical-align: middle;
      cursor: pointer;
      transition: color 0.3s;

      &:hover {
        color: @primary-color;
      }
    }
  }
}
</style>
