<template>
  <div class="new-page" :style="`min-height: ${pageMinHeight}px`">
    <h1 style="margin: 20px 20px 0 20px; font-weight: bold">欢迎光临！欢迎使用飨味通！</h1>
    <h2 style="margin: 20px 20px 0 20px; font-weight: bold">热销靓菜</h2>
    <a-carousel autoplay>
      <div v-for="dish in dishes" :key="dish.Did">
        <a-col>
          <a-row>
            <div class="image-container">
              <img :src="dish.picture" alt="Carousel Image">
            </div>
          </a-row>
          <a-row>
            <h3 style="margin: 0; font-size: 50px; color: black">{{ dish.Dname }}</h3>
          </a-row>
        </a-col>
      </div>
    </a-carousel>
    <a-row type="flex" justify="center">
      <a-button @click="handleJump" type="primary">去点菜</a-button>
    </a-row>
  </div>
</template>

<script>
import {mapState} from 'vuex'
import axios from "axios";
import {message} from "ant-design-vue";

export default {
  name: 'Demo',
  i18n: require('./i18n'),
  components: {},
  data() {
    return {
      // dishList: [
      //   // {id: 1, name: "apple", pic: "1.jpg"},
      //   // {id: 2, name: "orange", pic: "2.jpg"},
      //   // {id: 3, name: "fried chicken", pic: "3.jpg"},
      //   // {id: 4, name: "burger", pic: "4.jpg"}
      // ],
      dishes: {}
    };
  },
  created() {
    this.fetchDishData();
  },
  computed: {
    ...mapState('setting', ['pageMinHeight']),
    desc() {
      return this.$t('description')
    }
  },
  methods: {
    getImagePath(pic) {
      return require(`@/assets/dishPics/${pic}`);
    },
    handleJump() {
      this.$router.push('/dishes')
    },
    async fetchDishData() {
      try {
        const response = await axios.get('GetDishDisplay/');
        const dishes = {};
        response.data.dishList.forEach((dish) => {
          dishes[dish.Did] = dish;
        })
        this.dishes = dishes;
      } catch (error) {
        console.error('Error fetching dish data:', error);
        message.error('Failed to fetch dish data.');
      }
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

  h1 {
    font-size: 48px;
    color : #13C2C2;
  }
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}
</style>

<style scoped>
.ant-carousel >>> .slick-slide {
  text-align: center;
  height: 400px;
  line-height: 400px;
  background: #bebebe;
  overflow: hidden;
}

.ant-carousel >>> .slick-slide h3 {
  color: #fff;
}
</style>