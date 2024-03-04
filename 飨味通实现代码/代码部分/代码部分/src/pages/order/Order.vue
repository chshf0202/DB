<template>
  <div class="modal-font">
    <p style="font-family: Times New Roman fangsong; font-weight: bold; font-size: 20px;">订单</p>
    <p class="dish-name">共{{ ordersNum }}份订单</p>
    <a-row v-for="order in orders" :key="order.Oid" class="dish-row">
      <!-- 左侧图片列 -->
      <div v-for="dish in order.dishes" :key="dish.Did">
        <a-col :span="Object.keys(order.dishes).length === 2 ? 3 : 6">
          <img :src="dish.picture" alt="dish" class="dish-order-image" @click="dishOrderModal(order)">
        </a-col>
      </div>
        <a-col :span="2" offset="5">
          <p class="dish-name">{{ order.time }}</p>
          <!-- 操作按钮（点菜、加减数量等） -->
        </a-col>
        <!-- 右侧信息列 -->
        <a-col :span="6" offset="5">
          <!-- 菜品名字 -->
          <p class="dish-name">订单号:{{ order.Oid }}</p>
          <!-- 菜品价格 -->
          <p class="dish-price">￥{{ order.total }}</p>
          <!-- 操作按钮（点菜、加减数量等） -->
        </a-col>
    </a-row>

    <!--    <a-modal class="modal-font" v-model="dishOrderModalVisible"-->
    <!--             @ok="handelOrderInfoModal()" @cancel="handelOrderInfoModal()">-->
    <!--      <p style="font-family: Times New Roman fangsong; font-weight: bold; font-size: 20px;">历史订单</p>-->
    <!--      <p class="dish-name">共10样菜</p>-->
    <!--      <a-row v-for="dish in this.selectedOrder.dishes" :key="dish.Did" class="dish-row">-->
    <!--        &lt;!&ndash; 左侧图片列 &ndash;&gt;-->
    <!--        <a-col :span="6">-->
    <!--          <img :src="dish.picture" alt="dish" class="dish-order-image">-->
    <!--        </a-col>-->
    <!--        &lt;!&ndash; 中间信息列 &ndash;&gt;-->
    <!--        <a-col :span="9" class="dish-info">-->
    <!--          &lt;!&ndash; 菜品名字 &ndash;&gt;-->
    <!--          <p class="dish-name">{{ dish.name }}</p>-->
    <!--          &lt;!&ndash; 菜品价格 &ndash;&gt;-->
    <!--          <p class="dish-price">￥{{ dish.price }}</p>-->
    <!--        </a-col>-->
    <!--      </a-row>-->
    <!--      <p style="font-family: Times New Roman fangsong; font-weight: bold; font-size: 20px;">￥634</p>-->
    <!--    </a-modal>-->
  </div>
</template>

<script>
import axios from "axios";
import {message} from "ant-design-vue";
import {mapGetters} from "vuex";

export default {
  data() {
    return {
      selectedCategory: 'all',
      orders: {
        1: {
          Oid: 1,
          total: 1,
          time: "2002-01-01",
          dishes: {
            1: {Did: 1,
              Dname: "苹果",
              price: 3,
              description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
                  "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。",
              score: 4.6,
              star: 23,
              picture: "1.jpg",},
            2: {Did: 1,
              Dname: "苹果",
              price: 3,
              description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
                  "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。",
              score: 4.6,
              star: 23,
              picture: "1.jpg",},
            3: {Did: 1,
              Dname: "苹果",
              price: 3,
              description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
                  "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。",
              score: 4.6,
              star: 23,
              picture: "1.jpg",},
            4: {Did: 1,
              Dname: "苹果",
              price: 3,
              description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
                  "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。",
              score: 4.6,
              star: 23,
              picture: "1.jpg",}
          }
        },
        2: {
          Oid: 1,
          total: 1,
          time: "2002-01-01",
          dishes: {
            1: {Did: 1,
              Dname: "苹果",
              price: 3,
              description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
                  "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。",
              score: 4.6,
              star: 23,
              picture: "1.jpg",},
            2: {Did: 1,
              Dname: "苹果",
              price: 3,
              description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
                  "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。",
              score: 4.6,
              star: 23,
              picture: "1.jpg",},
            3: {Did: 1,
              Dname: "苹果",
              price: 3,
              description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
                  "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。",
              score: 4.6,
              star: 23,
              picture: "1.jpg",},
            4: {Did: 1,
              Dname: "苹果",
              price: 3,
              description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
                  "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。",
              score: 4.6,
              star: 23,
              picture: "1.jpg",}
          }
        }
      },
      // dishes: [
      //   {id: 1, image: "1.jpg", selected: false, category: "热菜", quantity: 0, name: "苹果", price: "40"},
      //   {id: 2, image: "2.jpg", selected: false, category: "小炒", quantity: 0, name: "橘子", price: "44"},
      //   {id: 3, image: "3.jpg", selected: false, category: "甜品", quantity: 0, name: "炸鸡", price: "86"},
      //   {id: 4, image: "4.jpg", selected: false, category: "热菜", quantity: 0, name: "汉堡", price: "68"},
      //   {id: 5, image: "5.jpg", selected: false, category: "热菜", quantity: 0, name: "鱼籽", price: "45"},
      //   {id: 6, image: "6.jpg", selected: false, category: "热菜", quantity: 0, name: "拉面", price: "234"},
      //   {id: 7, image: "7.jpg", selected: false, category: "热菜", quantity: 0, name: "鳗鱼", price: "234"},
      //   {id: 8, image: "8.jpg", selected: false, category: "热菜", quantity: 0, name: "炖菜", price: "34"},
      //   {id: 9, image: "9.jpg", selected: false, category: "热菜", quantity: 0, name: "蛋糕", price: "12"},
      //   {id: 10, image: "10.jpg", selected: false, category: "小炒", quantity: 0, name: "抹茶", price: "32"},
      //   {id: 11, image: "11.jpg", selected: false, category: "甜品", quantity: 0, name: "螃蟹", price: "54"},
      //   {id: 12, image: "12.jpg", selected: false, category: "热菜", quantity: 0, name: "烤鸭", price: "76"},
      //   {id: 13, image: "13.jpg", selected: false, category: "热菜", quantity: 0, name: "臭豆腐", price: "33"},
      // ],
      dishOrderModalVisible: false,
      userId: this.user.id,
      selectedOrder: null,
      ordersNum:0,
    };
  },
  computed: {
    ...mapGetters('account', ['user']),
    desc() {
      return this.$t('description')
    },
  },
  created() {
    this.userId = this.user.id;
    this.fetchOrderData({
      Uid: this.userId,
    })
    // this.loadData()
  },
  // beforeMount() {
  //     if (this.ordersNum > 0) {
  //       // 执行相关的操作
  //       console.log(this.ordersNum);
  //     }
  // },
  methods: {
    // async loadData() {
    //   try {
    //     await this.fetchOrderData({
    //       Uid: this.userId,
    //     })
    //         .then(() => {
    //           this.ordersNum = Object.keys(this.orders).length;
    //         })
    //     console.log(this.ordersNum)
    //     // 在这里进行其他与渲染相关的操作
    //   } catch (error) {
    //     console.error('Error fetching order data:', error);
    //   }
    // },

    getImagePath(pic) {
      return require(`@/assets/dishPics/${pic}`);
    },
    handelOrderInfoModal() {
      setTimeout(() => {
        this.dishOrderModalVisible = false;
        this.showComments = false; /* 这个变量的意义不确定 */
      }, 100);
    },
    dishOrderModal(order) {
      this.selectedOrder = order;
      this.dishOrderModalVisible = true;
    },
    async fetchOrderData(Uid) {
      try {
        const response = await axios.get(`GetUserOrder/?Uid=${Uid.Uid}`);
        const orders = {};
        console.log(response.data)
        response.data.orderList.forEach(order => {
          orders[order.Oid] = {
            Oid: order.Oid,
            total: order.total,
            time: order.time,
            dishes: {}, // Create an empty dishes object for each order
          };
          order.dishList.forEach(dish => {
              orders[order.Oid].dishes[dish.Did] = {
                Did: dish.Did,
                number: dish.number,
                picture: dish.picture
            }
          });
        });
        this.orders = orders;
        console.log(this.orders)
        this.ordersNum = Object.keys(this.orders).length;
      } catch (error) {
        console.error('Error fetching dish data:', error);
        message.error('Failed to fetch dish data.');
      }
    },
  }
}
</script>

<style scoped>

.modal-font {
  font-family: "Times New Roman", fangsong;
}

.dish-row {
  border-bottom: 1px solid #e8e8e8; /* 添加底部边框分隔每行菜品 */
  padding: 16px 0; /* 调整每行上下边距 */
}

.dish-order-image {
  max-width: 100px; /* 设置最大宽度，保持图片大小一致 */
  width: 100%; /* 图片宽度充满整个列 */
  height: 100%;
  max-height: 60px; /* 用最大高度把过高的图片强行卡成和其他图片一样高 */
  object-fit: cover;
}

.dish-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px; /* 调整名字和价格之间的垂直间距 */
}

.dish-price {
  font-size: 14px;
  color: #888; /* 添加灰色字体颜色 */
}

</style>