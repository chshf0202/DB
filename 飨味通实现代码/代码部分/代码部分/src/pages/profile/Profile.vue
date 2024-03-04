<template>
  <div class="new-page" :style="`min-height: ${pageMinHeight}px`">
    <h2 style="margin: 20px; font-weight: bold; border-bottom: 1px solid #e1e1db">
      {{ getCurrentTimeString() }}，{{ userInfo.name }}</h2>
    <a-row style="padding: 40px">
      <a-col :span="14">
        <div class="attribute-block">
          <a-row>
            <a-col :span="6">用户名</a-col>
            <a-col :span="14" style="color: #1f1f1f; font-size: 16px">{{ userInfo.name }}</a-col>
            <a-col :span="1" :offset="3">
              <a-button size="small" @click="editName">
                <a-icon type="edit"></a-icon>
              </a-button>
            </a-col>
          </a-row>
        </div>
        <div class="attribute-block">
          <a-row>
            <a-col :span="6">手机号</a-col>
            <a-col :span="14" style="color: #1f1f1f; font-size: 16px">{{ userInfo.phone }}</a-col>
            <a-col :span="1" :offset="3">
              <a-button size="small" @click="editPhone">
                <a-icon type="edit"></a-icon>
              </a-button>
            </a-col>
          </a-row>
        </div>
<!--        <div class="attribute-block">-->
<!--          <a-row>-->
<!--            <a-col :span="6">邮箱</a-col>-->
<!--            <a-col :span="14" style="color: #1f1f1f; font-size: 16px">{{ userInfo.email }}</a-col>-->
<!--            <a-col :span="1" :offset="3">-->
<!--              <a-button size="small" @click="editEmail">-->
<!--                <a-icon type="edit"></a-icon>-->
<!--              </a-button>-->
<!--            </a-col>-->
<!--          </a-row>-->
<!--        </div>-->
        <div class="attribute-block">
          <a-row>
            <a-col :span="6">密码</a-col>
            <a-col :span="14" style="color: #1f1f1f; font-size: 16px">{{ userInfo.password }}</a-col>
            <a-col :span="1" :offset="3">
              <a-button size="small" @click="editPwd">
                <a-icon type="edit"></a-icon>
              </a-button>
            </a-col>
          </a-row>
        </div>
        <a-row style="margin-top: 20px">
          <a-col :offset="19">
            <a-button @click="handleChangePicture">
              <a-icon type="picture"></a-icon>
              修改头像
            </a-button>
          </a-col>
        </a-row>
      </a-col>
      <a-col :span="7" :offset="1">
        <div class="user-image-container">
          <img :src="getImagePath(userInfo.picture)" alt="Dish image" class="user-image">
        </div>
      </a-col>
    </a-row>

    <!--             modals              -->
    <a-modal class="modal-font" v-model="chgNameVisible" title="修改用户名" :width="450"
             @ok="handleEditNameOk" @cancel="handleEditNameCancel">
      <a-input v-model="newName" placeholder="请输入新用户名"></a-input>
    </a-modal>

    <a-modal class="modal-font" v-model="chgPhoneVisible" title="修改手机号" :width="450"
             @ok="handleEditPhoneOk" @cancel="handleEditPhoneCancel">
      <a-input v-model="newPhone" placeholder="请输入新手机号"></a-input>
    </a-modal>

    <!--    <a-modal class="modal-font" v-model="chgEmailVisible" title="修改邮箱" :width="450"-->
    <!--             @ok="handleEditEmailOk" @cancel="handleEditEmailCancel">-->
    <!--      <a-input v-model="newEmail" placeholder="请输入新邮箱"></a-input>-->
    <!--    </a-modal>-->

    <a-modal class="modal-font" v-model="chgPwdVisible" title="修改密码" :width="450"
             @ok="handleEditPwdOk" @cancel="handleEditPwdCancel">
      <a-input v-model="newPwd" placeholder="请输入新密码" type="password"></a-input>
      <a-input v-model="newPwd2" placeholder="请再次输入新密码" type="password" style="margin-top: 20px"></a-input>
    </a-modal>

    <a-modal class="modal-font" v-model="chgPictureVisible" title="修改头像" :width="450"
             @ok="handleChangePictureOk" @cancel="handleChangePictureCancel">
      <a-upload :file-list="newPicture" show-upload-list="false" :before-upload="beforeUploadPicture">
        <a-button icon="upload">上传图片</a-button>
      </a-upload>
      <div v-if="newPicture">
        <img :src="newPicture.url" alt="New Dish Picture"
             style="max-width: 200px; max-height: 200px; margin-top: 10px;">
      </div>
    </a-modal>
  </div>
</template>

<script>
import {mapState} from 'vuex'
import axios from "axios";
import {message} from "ant-design-vue";
import {mapGetters} from "vuex";
import {mapMutations} from 'vuex'

export default {
  name: 'Profile',
  data() {
    return {
      userId: null,
      editing: false,
      userInfo: {
        // name: '吴际',
        // picture: '1.jpg',
        // phone: '10101010101',
        // password: '123456',
        // email: 'oowujioo@buaa.edu.cn'
      },

      chgNameVisible: false,
      newName: null,
      chgPhoneVisible: false,
      newPhone: null,
      chgEmailVisible: false,
      newEmail: null,
      chgPwdVisible: false,
      newPwd: null,
      newPwd2: null,
      chgPictureVisible: false,
      newPicture: null,
    }
  },
  computed: {
    ...mapState('setting', ['pageMinHeight']),
    ...mapGetters('account', ['user']),
    desc() {
      return this.$t('description')
    }
  },
  created() {
    this.init();
  },
  methods: {
    ...mapMutations('account', ['setUser']),
    async init() {
      this.userId = this.user.id;
      this.userInfo = {
        name: this.user.name,
        picture: null,
        phone: this.user.phone,
        password: this.user.password,
      }
      if (this.user.picUrl != null) {
        this.userInfo.picture = this.user.picUrl;
      } else {
        this.userInfo.picture = this.user.picture;
      }

    },
    beforeUploadPicture(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.newPicture = ({id: Date.now(), url: e.target.result});
      };
      reader.readAsDataURL(file);
      return true;
    },
    async changeUserName() {
      try {
        const request = {Uid: this.userId, Uname: this.newName};
        const response = await axios.post('ChangeUserUname/', request);
        if (!response.data.value) {
          message.success('修改成功'); // TODO: reload
          const user = {
              'id': this.user.id,
              'password': this.user.password,
              'name': this.newName,
              'picture': this.user.picture,
              'picUrl': this.user.picUrl,
              'phone': this.user.phone,
          }
          this.setUser(user);
          this.userInfo.name = this.user.name;
          location.reload();
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async changeUserPhone() {
      try {
        const request = {Uid: this.userId, phone: this.newPhone};
        const response = await axios.post('ChangeUserPhone/', request);
        if (!response.data.value) {
          message.success('修改成功'); // TODO: reload
          const user = {
            'id': this.user.id,
            'password': this.user.password,
            'name': this.user.name,
            'picture': this.user.picture,
            'picUrl': this.user.picUrl,
            'phone': this.newPhone,
          }
          this.setUser(user);
          this.userInfo.phone = this.user.phone;
          location.reload();
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    // async changeUserEmail() {
    //   try {
    //     const request = {Uid: this.userId, email: this.newEmail};
    //     const response = await axios.post('ChangeUserEmail/', request);
    //     if (!response.data.value) {
    //       message.success('修改成功'); // TODO: reload
    //       location.reload();
    //     } else {
    //       message.error(response.data.message);
    //     }
    //   } catch (error) {
    //     message.error('Error loading data from the database:', error);
    //   }
    // },
    async changeUserPwd() {
      try {
        const request = {Uid: this.userId, pwd: this.newPwd};
        const response = await axios.post('ChangeUserPwd/', request);
        if (!response.data.value) {
          message.success('修改成功'); // TODO: reload
          const user = {
            'id': this.user.id,
            'password': this.newPwd,
            'name': this.user.name,
            'picture': this.user.picture,
            'picUrl': this.user.picUrl,
            'phone': this.user.phone,
          }
          this.setUser(user);
          this.userInfo.password = this.user.password;
          location.reload();
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async changeUserPicture() {
      try {
        const request = {Uid: this.userId, picture: this.newPicture.url};
        const response = await axios.post('UploadUserPicture/', request);
        if (!response.data.value) {
          message.success('修改成功'); // TODO: reload
          const user = {
            'id': this.user.id,
            'password': this.user.password,
            'name': this.user.name,
            'picture': this.newPicture.url,
            'picUrl': null,
            'phone': this.user.phone,
          }
          this.setUser(user);
          this.userInfo.picture = this.user.picture;
          location.reload();
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    getImagePath(pic) {
      if (pic === 'default.jpg') {
        return require(`@/assets/img/${pic}`);
      } else {
        return pic;
      }
    },
    getCurrentTimeString() {
      const currentHour = new Date().getHours();
      if (currentHour >= 6 && currentHour < 12) {
        return '早上好';
      } else if (currentHour >= 12 && currentHour < 18) {
        return '下午好';
      } else {
        return '晚上好';
      }
    },
    /*---------edit name--------*/
    editName() {
      this.chgNameVisible = true;
    },
    handleEditNameOk() {
      if (!this.newName.trim()) {
        message.warn('请填写用户名');
        return;
      }
      this.changeUserName();
      this.chgNameVisible = false;
      setTimeout(() => {
        location.reload();
      }, 300);
    },
    handleEditNameCancel() {
      setTimeout(() => {
        this.newName = null;
      }, 300);
    },
    /*---------edit phone--------*/
    editPhone() {
      this.chgPhoneVisible = true;
    },
    handleEditPhoneOk() {
      if (!this.newPhone.trim()) {
        message.warn('请填写手机号');
        return;
      }
      this.changeUserPhone();
      this.chgPhoneVisible = false;
      setTimeout(() => {
        location.reload();
      }, 300);
    },
    handleEditPhoneCancel() {
      setTimeout(() => {
        this.newPhone = null;
      }, 300);
    },
    /*---------edit email--------*/
    editEmail() {
      this.chgEmailVisible = true;
    },
    handleEditEmailOk() {
      if (!this.newEmail.trim()) {
        message.warn('请填写邮箱');
        return;
      }
      this.changeUserEmail();
      this.chgEmailVisible = false;
      setTimeout(() => {
        location.reload();
      }, 300);
    },
    handleEditEmailCancel() {
      setTimeout(() => {
        this.newEmail = null;
      }, 300);
    },
    /*---------edit pwd--------*/
    editPwd() {
      this.chgPwdVisible = true;
    },
    handleEditPwdOk() {
      if (!this.newPwd.trim()) {
        message.warn('请填写密码');
        return;
      } else if (!this.newPwd2.trim()) {
        message.warn('请二次填写密码');
        return;
      } else if (this.newPwd !== this.newPwd2) {
        message.warn('两次输入密码不一致');
        return;
      }
      this.changeUserPwd();
      this.chgPwdVisible = false;
      setTimeout(() => {
        location.reload();
      }, 800);
    },
    handleEditPwdCancel() {
      setTimeout(() => {
        this.newPwd = null;
        this.newPwd2 = null;
      }, 300);
    },
    /*--------- edit picture ----------*/
    handleChangePicture() {
      this.chgPictureVisible = true;
    },
    handleChangePictureOk() {
      this.changeUserPicture();
      this.chgPictureVisible = false;
      setTimeout(() => {
        location.reload();
      }, 300);
    },
    handleChangePictureCancel() {

    },
    beforeUploadDishPicture(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.newPicture = ({id: Date.now(), url: e.target.result});
      };
      reader.readAsDataURL(file);
      return true;
    },
  }
}

</script>

<style scoped lang="less">
.new-page {
  height: 100%;
  background-color: @base-bg-color;
  padding: 10px 0;
  border-radius: 4px;
  font-family: "Times New Roman", fangsong;
}

.attribute-block {
  border-bottom: #e1e1db 1px solid;
  padding: 20px 20px 15px 20px;
  font-weight: bolder;
}

.user-image-container {
  overflow: hidden;
  border-radius: 50%;
  width: 250px;
  height: 250px;
  margin: 10px 0 20px 20px;
}

.user-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-font {
  font-family: "Times New Roman", fangsong;
}
</style>