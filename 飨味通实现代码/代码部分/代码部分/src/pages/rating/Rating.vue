<template>
  <div class="new-page" :style="`min-height: ${pageMinHeight}px`">
    <h2 style="margin: 20px; font-weight: bold">评价中心</h2>
    <h3 style="padding: 0 0 20px 20px">
      {{ (Object.keys(dishList).length) ? '以下是您已点过的菜：' : '您还没有点过任何菜品。' }}
    </h3>

    <a-row :gutter="16" style="text-align: center">
      <a-col :span="6" v-for="dish in dishList" :key="dish.Did" style="padding: 15px 0">
        <div class="image-block">
          <img :src="dish.picture" alt="Dish image" class="dish-image">
        </div>
        <a-row style="display: flex; align-items: center;">
          <a-col :span="12" :offset="6">
            <div style="margin: 0; font-size: 20px">{{ dish.Dname }}</div>
          </a-col>
          <a-col :span="4" style="color: #ffc109">
            <a-icon type="star" theme="filled"></a-icon>
            {{ dish.score }}
          </a-col>
        </a-row>
        <a-row>
          <a-col :span="4" :offset="4">
            <a-button type="primary" size="small" @click="handleInfo(dish.Did)">详情</a-button>
          </a-col>
          <a-col :span="4" :offset="8">
            <a-button type="primary" size="small" @click="handleRate(dish.Did)">评价</a-button>
          </a-col>
        </a-row>
      </a-col>
    </a-row>

    <a-modal v-if="dishInfo" class="modal-font" v-model="infoModalVisible" title="详情" :width="650"
             @ok="handleCloseInfo" @cancel="handleCloseInfo" :cancel-button-props="{ style: { display: 'none' } }">
      <a-row>
        <a-col :span="10" style="margin-bottom: 20px">
          <div class="image-block">
            <img :src="dishInfo.picture" alt="Dish image" class="dish-image">
          </div>
        </a-col>
        <a-col :span="13" :offset="1">
          <a-row>
            <a-col :span="12">
              <div style="font-weight: bolder; font-size: 20px;">
                <span style="font-size: 20px">{{ dishInfo.Dname }} </span>
                <span style="font-size: 16px">￥{{ dishInfo.price }}</span>
              </div>
            </a-col>
            <a-col :span="4" :offset="7">
              <a-button size="small" @click="star" id="star-button"
                        :style="{borderColor: 'transparent',color: isStarred ? '#ffc109' : '#8c8c8c'}">
                <div>
                  <a-icon type="star" :theme="isStarred ? 'filled' : ''"></a-icon>
                  {{ dishInfo.star }}
                </div>
              </a-button>
            </a-col>
          </a-row>
          <a-row>
            <div style="color: #ffc109">
              <a-rate v-model="roundedScore" :disabled="true" :allow-half="true" style="font-size: 14px"></a-rate>
              <span style="margin-left: 10px; font-size: 14px">{{ dishInfo.score }}</span>
            </div> <!-- TODO: is roundedScore here correct?-->
            <div style="font-size: 15px; color: #8c8c8c; margin-top: 10px">“{{ dishInfo.description }}”</div>
            <div style="margin-top: 10px">
              <div v-for="tag in dishTag" :key="tag.id" class="custom-tag"
                   :style="{ color: tagColors[tag.id], border: `1px solid ${tagColors[tag.id]}` }">
                {{ tag.Tname }}
              </div>
            </div>
          </a-row>
        </a-col>
      </a-row>

      <a-button @click="toggleComments" size="small">
        <span style="font-size: 15px">评价</span>
        <a-icon :type="showComments ? 'up' : 'down'"/>
      </a-button>
      <div v-show="showComments">
        <a-row v-for="comment in dishComments" :key="comment.Cid">
          <a-row style="border-top: #eaeae4 solid 1px; margin-top: 10px; padding: 10px 0">
            <a-col :span="3">
              <div class="user-image-container">
                <img :src="getImagePath(comment.userPic)" alt="userPic" class="user-image">
              </div>
            </a-col>
            <a-col :span="21">
              <div style="color: black">{{ comment.Uname }}</div>
              <div style="color: #ffc109">
                <a-icon type="star" theme="filled"></a-icon>
                {{ comment.score }}
              </div>
              <div style="color: #8c8c8c">{{ comment.content }}</div>
              <div class="uploaded-images-container" style="margin-top: 10px">
                <div v-for="image in comment.pictureList" :key="image">
                  <div class="image-wrapper">
                    <img :src="image" alt="image" class="thumbnail">
                  </div>
                </div>
              </div>
              <div v-show="comment.Uid === userId">
                <a-button  type="danger" icon="delete" style="float: right" @click="deleteComment(comment)"></a-button>
              </div>
            </a-col>
          </a-row>
        </a-row>
      </div>
    </a-modal>

    <a-modal class="modal-font" v-model="rateModalVisible" title="评论" @ok="handleRateOk" @cancel="handleRateCancel">
      <a-rate v-model="starRating" :count="5" style="margin-bottom: 10px"/>
      <a-textarea v-model="input" placeholder="请输入评论内容" :autosize="{ minRows: 4, maxRows: 6}"
                  style="margin-bottom: 10px"></a-textarea>
      <a-upload :before-upload="handleBeforeUpload" :file-list="uploadedImages">
        <a-button>
          <a-icon type="picture"></a-icon>
        </a-button>
      </a-upload>
      <div class="uploaded-images-container" style="margin-top: 10px">
        <div v-for="image in uploadedImages" :key="image.id" class="image-container">
          <span class="delete-button" @click="handleDeleteImage(image.id)">
            <a-icon type="delete" class="delete-icon"></a-icon>
          </span>
          <div class="image-wrapper">
            <img :src="image.url" alt="image" class="thumbnail">
          </div>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script>
import {message} from "ant-design-vue";
import axios from "axios";
import {mapState, mapGetters} from 'vuex';

export default {
  name: 'Rating',
  data() {
    return {
      // init
      userId: null,
      userName: null,
      dishList: {
        // 1: {
        //   Did: 1,
        //   Dname: "苹果",
        //   price: 3,
        //   description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
        //       "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。",
        //   score: 4.6,
        //   star: 23,
        //   picture: "1.jpg",
        // },
        // 2: {
        //   Did: 2,
        //   Dname: "橘子",
        //   price: 3,
        //   description: "null",
        //   score: 4.7,
        //   star: 0,
        //   picture: "2.jpg",
        // },
        // 3: {
        //   Did: 3,
        //   Dname: "炸鸡炸鸡炸鸡炸",
        //   price: 10,
        //   description: "Fried chicken, also known as Southern fried chicken, " +
        //       "is a dish consisting of chicken pieces that have been coated with seasoned flour or batter and pan-fried, deep fried, pressure fried, or air fried.",
        //   score: 2.1,
        //   star: 99,
        //   picture: "3.jpg",
        // },
        // 4: {Did: 4, Dname: "汉堡", picture: "4.jpg", score: 3.3, price: 15, star: 18, description: "null"}
      },

      // for both modals
      curDishId: 0,
      // comment modal
      rateModalVisible: false,
      input: null,
      starRating: 0,
      uploadedImages: [],

      // info modal
      infoModalVisible: false,
      dishInfo: null,
      dishTag: [
        {Tid: 1, Tname: '不辣'},
        {Tid: 2, Tname: '清真'}
      ],
      tagColors: {},
      roundedScore: 0,
      showComments: false,
      dishComments: [
        // {id: 100, score: 4.5, content: "tastes like apple", userName: "匿名用户", userPic: "1.jpg", images: []},
        // {id: 101, score: 4.5, content: "tastes like apple", userName: "匿名用户", userPic: "1.jpg", images: ["1.jpg"]},
        // {
        //   id: 102,
        //   score: 4.5,
        //   content: "tastes like apple",
        //   userName: "匿名用户",
        //   userPic: "1.jpg",
        //   images: ["1.jpg", "2.jpg", "3.jpg", "4.jpg"]
        // },
      ],
      isStarred: false,
    }
  },
  created() {
    this.init();
    this.generateRandomColors();
  },
  watch: {
    'dishInfo.score'(newValue) {
      this.roundedScore = this.round(newValue);
    },
    'dishTag'() {
      this.generateRandomColors();
    }
  },
  computed: {
    ...mapState('setting', ['pageMinHeight']),
    ...mapGetters('account', ['user']),
    desc() {
      return this.$t('description')
    },
  },

  methods: {
    async init() {
      try {
        this.userId = this.user.id;
        this.userName = this.user.name;
        const response = await axios.get(`GetUserOrderedDish/?Uid=${this.userId}`);
        const dishList = {};
        response.data.dishList.forEach((dish) => {
          dishList[dish.Did] = dish;
        })
        this.dishList = dishList;
        // this.dishList = response.data.dishList;
        // message.success("init succeed");
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async getDishTag() {
      try {
        const request = {Did: this.curDishId};
        // message.success(this.curDishId)
        const response = await axios.post('GetDishTag/', request);
        this.dishTag = response.data.tagList;
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async getDishComment() {
      try {
        const request = {Did: this.curDishId};
        const response = await axios.post('GetDishComment/', request);
        this.dishComments = response.data.commentList;
        console.log(response)
        console.log(this.dishComments)
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async getStar() {
      try {
        const request = {Uid: this.userId, Did: this.curDishId};
        const response = await axios.post('GetStar/', request);
        this.isStarred = response.data.isStared;
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async userStarDish() {
      try {
        const request = {Uid: this.userId, Did: this.curDishId};
        // message.success(this.userId)
        const response = await axios.post('UserStarDish/', request);
        if (!response.data.value) {
          message.success('收藏成功');
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async userUnstarDish() {
      try {
        const request = {Uid: this.userId, Did: this.curDishId};
        const response = await axios.post('UserUnstarDish/', request);
        if (!response.data.value) {
          message.success('取消收藏成功');
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async rate() {
      try {
        const request = {Uid: this.userId, Did: this.curDishId, content: this.input, score: this.starRating};
        const pictureList = [];
        this.uploadedImages.forEach((image) => {
          pictureList.push(image.url);
        });
        request["pictureList"] = pictureList;
        const response = await axios.post('AddComment/', request);
        if (!response.data.value) {
          message.success('评论成功！');
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async deleteComment(comment) {
      try {
        // message.success(comment.Uid);
        // message.success(this.userId)
        // message.success(comment.userName);
        // message.success(this.userName);
        if (comment.Uid !== this.userId) {
          message.error('不能删除别人的评论！')
          return;
        }
        const request = {Cid: comment.Cid};
        const response = await axios.post('DeleteComment/', request);
        if (!response.data.value) {
          message.success('删除成功！');
          // location.reload()
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

    /*----------- rate ----------*/
    handleRate(dishId) {
      this.curDishId = dishId;
      this.rateModalVisible = true;
    },
    handleRateOk() {
      if (!this.input.trim()) {
        message.warn('请填写评论内容');
        return;
      } else if (this.starRating === 0) {
        message.warn('请选择评分');
        return;
      }
      this.rate();
      this.rateModalVisible = false;
      setTimeout(() => {
        this.input = null;
        this.starRating = 0;
        this.uploadedImages = [];
        // message.success('success!');
      }, 300);
    },
    handleRateCancel() {
      setTimeout(() => {
        this.input = null;
        this.starRating = 0;
        this.uploadedImages = [];
      }, 300);
    },
    handleBeforeUpload(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.uploadedImages.push({id: Date.now(), url: e.target.result});
      };
      reader.readAsDataURL(file);
      return true;
    },
    handleDeleteImage(imageId) {
      this.uploadedImages = this.uploadedImages.filter((image) => image.id !== imageId);

      // Update the fileList to remove the corresponding file TODO: what does this mean?
      // this.fileList = this.fileList.filter((file) => file.uid !== imageId);
    },

    /*----------- info ----------*/
    handleInfo(dishId) {
      this.curDishId = dishId;
      this.dishInfo = this.dishList[dishId];
      this.getStar();
      this.getDishTag();
      this.infoModalVisible = true;
    },
    handleCloseInfo() {
      this.infoModalVisible = false;
      setTimeout(() => {
        this.showComments = false;
      }, 300);
    },
    toggleComments() {
      if (!this.showComments) {
        this.getDishComment(this.curDishId);
      }
      this.showComments = !this.showComments;
    },
    round(score) {
      if (score < 0.5) {
        return 0.5;
      }
      return Math.round(score * 2) / 2;
    },
    star() {
      this.isStarred = !this.isStarred;
      if (this.isStarred) {
        this.userStarDish();
        this.$set(this.dishInfo, 'star', this.dishInfo.star + 1);
        //message.success('收藏成功！');
      } else {
        this.userUnstarDish();
        this.$set(this.dishInfo, 'star', this.dishInfo.star - 1);
        //message.success('收藏已取消！');
      }
    },
    randomColor() {
      const randomComponent = () => Math.floor(Math.random() * 200);
      return `rgb(${randomComponent()}, ${randomComponent()}, ${randomComponent()})`;
    },
    generateRandomColors() {
      const colors = {};
      this.dishTag.forEach((tag) => {
        colors[tag.id] = this.randomColor();
      });
      this.tagColors = colors;
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

.image-container {
  position: relative;
  display: inline-block;
  margin-right: 8px;
  text-align: center;
}

.delete-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  cursor: pointer;
}

.delete-icon {
  font-size: 16px;
  color: #bfbfbf;
  transition: color 0.3s;
}

.delete-button:hover .delete-icon {
  color: #fff;
}

.image-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.uploaded-images-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 8px;
}

.thumbnail {
  max-width: 100%;
  height: auto;
  margin-bottom: 8px;
}

.image-block {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dish-image {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: cover;
}

.user-image-container {
  overflow: hidden;
  border-radius: 50%;
  width: 50px;
  height: 50px;
}

.user-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-font {
  font-family: "Times New Roman", fangsong;
}

#star-button :hover {
  color: #ffc109;
  border-color: #ffc109
}

.custom-tag {
  display: inline-block;
  font-size: 10px;
  padding: 4px 10px;
  border-radius: 40px;
  margin-left: 10px;
}
</style>