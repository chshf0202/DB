<!-- DishMenu.vue -->

<template>
  <div class="dish-menu">
    <a-tabs v-model="selectedCategory" @change="handleChangeCategory">
      <a-tab-pane key="all" tab="All">
        <div class="dish-container">
          <div v-for="dish in dishes" :key="dish.Did" class="dish-item">
            <img :src="dish.picture" alt="dish" class="dish-image" style="max-width: 250px"
                 @click="dishModal()">
            <a-row style="display: flex; align-items: center;">
              <a-col :span="4" :offset="1">
                <h3>￥{{ dish.price }}</h3>
              </a-col>
              <a-col :span="8" :offset="3">
                <h3 style="margin: 0; font-size: 20px; font-family: Times New Roman fangsong;">{{ dish.Dname }}</h3>
              </a-col>
              <a-col :span="4" :offset="3" style="color: #ffc109">
                <a-icon type="star" theme="filled"></a-icon>
                {{ dish.score }}
              </a-col>
            </a-row>
            <a-button v-if="dish.remain > 0" type="primary" class="minusIcon" @click="decreaseQuantity(dish)">
              <a-icon v-if="dish.remain > 0" type="minus-circle" class="icon-red"/></a-button>
            <span v-if="dish.remain > 0" class="quantity">{{ dish.quantity }}</span>
            <span v-else>售罄</span>
            <a-button v-if="dish.remain > 0" type="primary" class="plusIcon" @click="increaseQuantity(dish)">
              <a-icon v-if="dish.remain > 0" type="plus-circle" class="icon-red"/></a-button>
          </div>
        </div>
      </a-tab-pane>
      <a-tab-pane v-for="category in categories" :key="category.Gid" :tab="category.Gname">
        <div class="dish-container">
          <div v-for="dish in filteredDishesByCategory(category.Gid)" :key="dish.Did" class="dish-item">
            <img :src="dish.picture" alt="dish" class="dish-image" style="max-width: 250px"
                 @click="dishModal()">
            <a-row style="display: flex; align-items: center;">
              <a-col :span="4" :offset="1">
                <h3>￥{{ dish.price }}</h3>
              </a-col>
              <a-col :span="8" :offset="3">
                <h3 style="margin: 0; font-size: 20px; font-family: Times New Roman fangsong;">{{ dish.Dname }}</h3>
              </a-col>
              <a-col :span="4" :offset="3" style="color: #ffc109">
                <a-icon type="star" theme="filled"></a-icon>
                {{ dish.score }}
              </a-col>
            </a-row>
            <a-button v-if="dish.remain > 0" type="primary" class="minusIcon" @click="decreaseQuantity(dish)">
              <a-icon v-if="dish.remain > 0" type="minus-circle" class="icon-red"/></a-button>
            <span v-if="dish.remain > 0" class="quantity">{{ dish.quantity }}</span>
            <span v-else>售罄</span>
            <a-button v-if="dish.remain > 0" type="primary" class="plusIcon" @click="increaseQuantity(dish)">
              <a-icon v-if="dish.remain > 0" type="plus-circle" class="icon-red"/></a-button>
          </div>
        </div>
      </a-tab-pane>
    </a-tabs>

    <a-modal class="modal-font" v-model="dishModalVisible" title="菜品详情"
             @ok="handelInfoModal()" @cancel="handelInfoModal()">
      <a-row>
        <a-col :span="12" style="margin-bottom: 20px">
          <div class="image-block">
            <img :src="getImagePath(dishInfo.pic)" alt="Dish image" class="detail-dish-image">
          </div>
        </a-col>
        <a-col :span="12">
          <a-row>
            <a-col :span="12">
              <div style="font-weight: bolder; font-size: 20px;">{{ dishInfo.name }}</div>
            </a-col>
            <a-col :span="8" :offset="4">
              <div class="custom-button">
                <a-icon type="star"></a-icon>
                {{ dishInfo.score }}
              </div>
            </a-col>
          </a-row>
          <div style="font-weight: bolder; font-size: 16px;">
            ￥{{ dishInfo.price }}
          </div>
          <p style="font-size: 15px; color: #8c8c8c">"{{ dishInfo.description }}"</p>
        </a-col>
      </a-row>
    </a-modal>

    <a-affix :offset-bottom="0" class="modal-font">
      <a-button type="primary" style="font-weight: bolder; font-size: 16px; padding: 10px 10px 30px;"
                @click="dishOrderModal()">购物车/结账
        <a-icon type="shopping-cart"></a-icon>
      </a-button>
    </a-affix>

    <a-modal class="modal-font" v-model="dishOrderModalVisible"
             @ok="handelOrderInfoModalOk()" @cancel="handelOrderInfoModal()" okText="结账">
      <p style="font-family: Times New Roman fangsong; font-weight: bold; font-size: 20px;">购物车</p>
      <p class="dish-name">共{{ sumQuantity }}样菜</p>
      <a-row v-for="dish in filteredOrderDishes" :key="dish.Did" class="dish-row">
        <!-- 左侧图片列 -->
        <a-col :span="6">
          <img :src="dish.picture" alt="dish" class="dish-order-image">
        </a-col>
        <!-- 中间信息列 -->
        <a-col :span="9" class="dish-info">
          <!-- 菜品名字 -->
          <p class="dish-name">{{ dish.name }}</p>
          <!-- 菜品价格 -->
          <p class="dish-price">￥{{ dish.price }}</p>
        </a-col>
        <!-- 右侧数量操作列 -->
        <a-col :span="1" offset="2">
          <a-button type="primary" class="shoppingCartButton" @click="decreaseQuantity(dish)">
            <a-icon type="minus-circle" class="icon-red"/></a-button>
        </a-col>
        <a-col :span="1" offset="2">
          <span class="quantity">{{ dish.quantity }}</span>
        </a-col>
        <a-col :span="1" offset="0">
          <a-button type="primary" class="shoppingCartButton" @click="increaseQuantity(dish)">
            <a-icon type="plus-circle" class="icon-red"/></a-button>
        </a-col>
      </a-row>
      <p style="font-family: Times New Roman fangsong; font-weight: bold; font-size: 20px;">￥{{total}}</p>
    </a-modal>

  </div>
</template>

/*原来把button嵌套了，所以点菜按钮下面的+和-点不到，现在变成并列的，不把+和-放到点菜button环境中就可以了 */

<script>
import axios from 'axios';
import {message} from "ant-design-vue";
import {mapGetters} from "vuex";

export default {
  data() {
    return {
      selectedCategory: 'all',
      dishes: {
        1: {
        },
        2: {

        },
        3: {

        },
        4: {

        }
      },
      // dishes: [
        // {id: 1, image: "1.jpg", selected: false, category: "热菜", quantity: 0, name: "苹果", price: "40", score: "4.5", remain: "10"},
        // {id: 2, image: "2.jpg", selected: false, category: "小炒", quantity: 0, name: "橘子", price: "44", score: "4.5", remain: "10"},
        // {id: 3, image: "3.jpg", selected: false, category: "甜品", quantity: 0, name: "炸鸡", price: "86", score: "4.5", remain: "10"},
        // {id: 4, image: "4.jpg", selected: false, category: "热菜", quantity: 0, name: "汉堡", price: "68", score: "4.5", remain: "10"},
        // {id: 5, image: "5.jpg", selected: false, category: "热菜", quantity: 0, name: "鱼籽", price: "45", score: "4.5", remain: "10"},
        // {id: 6, image: "6.jpg", selected: false, category: "热菜", quantity: 0, name: "拉面", price: "234", score: "4.5", remain: "10"},
        // {id: 7, image: "7.jpg", selected: false, category: "热菜", quantity: 0, name: "鳗鱼", price: "234", score: "4.5", remain: "10"},
        // {id: 8, image: "8.jpg", selected: false, category: "热菜", quantity: 0, name: "炖菜", price: "34", score: "4.5", remain: "10"},
        // {id: 9, image: "9.jpg", selected: false, category: "热菜", quantity: 0, name: "蛋糕", price: "12", score: "4.5", remain: "10"},
        // {id: 10, image: "10.jpg", selected: false, category: "小炒", quantity: 0, name: "抹茶", price: "32", score: "4.5", remain: "10"},
        // {id: 11, image: "11.jpg", selected: false, category: "甜品", quantity: 0, name: "螃蟹", price: "54", score: "4.5", remain: "10"},
        // {id: 12, image: "12.jpg", selected: false, category: "热菜", quantity: 0, name: "烤鸭", price: "76", score: "4.5", remain: "10"},
        // {id: 13, image: "13.jpg", selected: false, category: "热菜", quantity: 0, name: "臭豆腐", price: "33", score: "4.5", remain: "10"},
      // ],
      categories: [
        {id: 1, name: "热菜"},
        {id: 2, name: "小炒"},
        {id: 3, name: "甜品"},
      ],
      dishInfo: {
        id: 1, name: "苹果", pic: "1.jpg", score: 4.5, price: 3,
        description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
            "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。"
      },
      dishModalVisible: false,
      dishOrderModalVisible: false,
      total: 0,
      sumQuantity: 0,
      userId: null,
    };
  },
  created() {
        this.fetchDishData(); // Call the function to fetch dish data when the component is created
        this.fetchCatagory();
          this.userId = this.user.id;
    },
  computed: {
    ...mapGetters('account', ['user']),
    filteredDishes() {
      return this.selectedCategory === 'all'
          ? Object.values(this.dishes)
          : Object.values(this.dishes).filter((dish) => dish.Gid === this.selectedCategory);
    },
    filteredOrderDishes() {
      return Object.values(this.dishes).filter(dish => dish.quantity > 0);
    },
  },
  methods: {
    getImagePath(pic) {
      return require(`@/assets/dishPics/${pic}`);
    },
    handleChangeCategory(value) {
      this.selectedCategory = value;
    },
    decreaseQuantity(dish) {
      // 减少数量
      if (dish.quantity >= 1) {
        dish.quantity--;
        this.sumQuantity--;
      }
    },
    async increaseQuantity(dish) {
      console.log('Toggle order button clicked for dish ID:', dish.Did);
      // 增加数量
      if(dish.quantity<dish.remain){
        dish.quantity++;
        this.sumQuantity++;
      } else {
        message.warning("库存不足")
      }
      this.total = 0;
      Object.values(this.dishes).forEach(d => {
        this.total += d.quantity * d.price;
      });
      // this.sendOrderToBackend({
      //   dishId: dish.Did,
      //   quantity: dish.quantity,
      //   category: dish.Gid,
      //   // 其他相关信息...
      // })
    },
    getOrderButtonContent(dish) {
      if (dish.quantity > 0) {
        // 如果数量大于0，显示"-quantity+"
        return `-${dish.quantity}+`;
      } else {
        // 如果数量为0，显示"+"
        return '+';
      }
    },
    orderDish(id) {
      const index = this.dishes.findIndex((dish) => dish.Did === id);
      if (index !== -1) {
        this.dishes[index].selected = !this.dishes[index].selected;
      }
    },
    filteredDishesByCategory(category) {
      return Object.values(this.dishes).filter((dish) => dish.Gid === category);
    },
    // async sendOrderToBackend(orderDetails) {
    //   try {
    //     const response = await axios.get('GetAllDish/', orderDetails);
    //     // this.dishes = response.data.dishList
    //     console.log('Order sent successfully:', response.data);
    //     message.success('点菜成功!');
    //   } catch (error) {
    //     console.error('Error sending order:', error);
    //   }
    // },
    dishModal() {
      this.dishModalVisible = true;
    },
    dishOrderModal() {
      this.dishOrderModalVisible = true;
    },
    handelInfoModal() {
      setTimeout(() => {
        this.dishModalVisible = false;
        this.showComments = false; /* 这个变量的意义不确定 */
      }, 100);
    },
    handelOrderInfoModal() {
      setTimeout(() => {
        this.dishOrderModalVisible = false;
        this.showComments = false; /* 这个变量的意义不确定 */
      }, 100);
    },
    handelOrderInfoModalOk() {
      setTimeout(() => {
        this.sendNewOrder({
          Uid: this.userId,
          total: this.total,
          dishList: Object.values(this.dishes).filter(dish => dish.quantity > 0).map(dish => ({ Did: dish.Did, number: dish.quantity })),
          // 其他相关信息...
        })
        Object.values(this.dishes).filter(dish => {
          if (dish.quantity > 0) {
            dish.remain -= dish.quantity; // 减去 quantity
            dish.quantity = 0; // 清零 quantity
          }
        });
        this.dishOrderModalVisible = false;
        this.showComments = false;
        message.success('结账成功!');
        this.$router.push('/demo'); // 修改这里的路径为 /demo
      }, 100);
    },
    async sendNewOrder(orderInfo) {
      try {
        await axios.post('AddOrder/', orderInfo);
        // this.dishes = response.data.dishList;
        // message.success(response.data.dishList.Did)
      } catch (error) {
        console.error('Error fetching dish data:', error);
        message.error('Failed to fetch dish data.');
      }
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
    async fetchCatagory() {
      try {
        const response = await axios.get('GetAllGroup/');
        this.categories = response.data.groupList;
        // message.success('获取Group成功')
      } catch (error) {
        console.error('Error fetching dish data:', error);
        message.error('Failed to fetch dish data.');
      }
    },
  },
};
</script>

<style scoped>
.dish-menu {
  padding: 20px;
}

.dish-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.dish-item {
  flex-basis: 25%; /* 根据需要调整每个 .dish-item 元素的基础大小 */
  text-align: center;
  margin-bottom: 50px; /* 这是我写的注释，可以调节图片和图片之间纵向的距离，50px是为了图片和图片之间可以塞入button */
  position: relative; /* 添加相对定位，使得按钮相对于父容器进行定位 */
}

.dish-image {
  width: 320px; /* 根据需要调整大小 */
  height: 150px; /* 根据需要调整大小 */
  object-fit: cover; /* 保持图片比例，裁剪填充容器 */
}

.dish-name {
  font-family: "Times New Roman", fangsong;
  font-weight: bold;
  font-size: 16px;
  top: 160px; /* 可根据需要调整上边距 */
}

.minusIcon {
  position: absolute; /* 使用绝对定位 */
  top: 180px; /* 这是我写的注释，可以调节按钮和图片的顶边之间纵向的距离，160px是为了刚好卡进图片和图片之间的距离 */
  left: 96px; /* 数据不能乱动，多个absolute的z轴堆叠原理我不明白，这个数据可以面向保证三个按钮不遮挡 */
  width: 20px;
  background-color: transparent;
  border: none;
}

.plusIcon {
  position: absolute;
  top: 180px; /* 这是我写的注释，可以调节按钮和图片的顶边之间纵向的距离，160px是为了刚好卡进图片和图片之间的距离 */
  left: 142px; /* 数据不能乱动，多个absolute的z轴堆叠原理我不明白，这个数据可以面向保证三个按钮不遮挡 */
  width: 20px;
  background-color: transparent;
  border: none;
}

.shoppingCartButton{
  background-color: transparent;
  border: none;
}

.image-block {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-button {
  display: inline-block;
  padding: 4px 12px;
  border: 1px solid #bfbfbf;
  border-radius: 20px;
}

.modal-font {
  font-family: "Times New Roman", fangsong;
}

.detail-dish-image {
  max-width: 250px;
  max-height: 250px;
  width: auto;
  height: auto;
  object-fit: cover;
}

.dish-row {
  margin-bottom: 10px;
}

.dish-info {
  padding-left: 10px; /* 调整左侧内边距 */
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

.quantity {
  font-weight: bold;
}

.icon-red {
  color: black; /* 将图标颜色设置为黑色 */
  font-size: 20px;
}

</style>



