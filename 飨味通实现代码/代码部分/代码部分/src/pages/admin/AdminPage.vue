<template>
  <div class="new-page" :style="`min-height: ${pageMinHeight}px`">
    <h2 style="font-weight: bold">管理员界面</h2>
    <a-row style="margin: 20px 0">
<!--      <a-col :span="5">-->
<!--        <a-input v-model="searchInput" placeholder="搜索菜品" style="width: 80%"></a-input>-->
<!--        <a-button icon="search" @click="handelSearch" style="width: 20%"></a-button>-->
<!--      </a-col>-->
      <a-col :span="7" :offset="17">
        <a-button @click="handleRegisterDish">添加菜品</a-button>
        <a-button @click="handleRegisterTag" style="margin-left: 10px">新建标签</a-button>
        <a-button @click="handleRegisterGroup" style="margin-left: 10px">新建菜品组</a-button>
      </a-col>
    </a-row>

    <a-row style="background-color: #fafafa" class="dish-table-row">
      <a-col :span="5">菜品名称</a-col>
      <a-col :span="9">标签</a-col>
      <a-col :span="4">库存</a-col>
      <a-col :span="6"></a-col>
    </a-row>
    <a-row v-for="dish in dishList" :key="dish.Did" class="dish-table-row">
      <a-col :span="5">{{ dish.Dname }}</a-col>
      <a-col :span="9">
        <div v-for="tag in dish.tagList" :key="tag.id" class="custom-tag"
             :style="{ color: tagColors[tag.id], border: `1px solid black` }">
          {{ tag.Tname }}
        </div>
      </a-col>
      <a-col :span="4">{{ dish.remain }}</a-col>
      <a-col :span="6">
        <a-button @click="handelAddInventory(dish.Did)" style="margin-left: 30px">
          <a-icon type="plus"></a-icon>
          添加库存
        </a-button>
        <a-button @click="handleAddTag2Dish(dish.Did)" style="margin-left: 10px">
          <a-icon type="tag"></a-icon>
          添加标签
        </a-button>
      </a-col>
    </a-row>

    <!--    modals-->
    <a-modal class="modal-font" v-model="registerDishVisible" title="注册菜品"
             @ok="handleRegisterDishOk" @cancel="handleRegisterDishCancel">
      <div>
        <a-input v-model="newDishName" placeholder="请输入菜品名称" style="width: 200px; margin-bottom: 20px"></a-input>
      </div>
      <a-input v-model="newDishPrice" placeholder="请输入菜品价格" style="width: 200px; margin-bottom: 20px"></a-input>
      <a-input v-model="newDishInventory" placeholder="请输入菜品库存"
               style="width: 200px; margin-left: 20px"></a-input>
      <a-textarea v-model="newDishDescription" placeholder="请输入菜品描述"
                  :autosize="{ minRows: 4, maxRows: 6}" style="margin-bottom: 20px"></a-textarea>
      <a-radio-group v-model="newDishGid" style="margin-bottom: 20px">
        <a-radio v-for="group in allGroups" :key="group.Gid" :value="group.Gid">{{ group.Gname }}</a-radio>
      </a-radio-group>
      <div>
        <a-upload :file-list="newDishPicture" show-upload-list="false" :before-upload="beforeUploadDishPicture">
          <a-button icon="upload">上传图片</a-button>
        </a-upload>
      </div>
      <div v-if="newDishPicture">
        <img :src="newDishPicture.url" alt="New Dish Picture"
             style="max-width: 200px; max-height: 200px; margin-top: 10px;">
      </div>
    </a-modal>

    <a-modal class="modal-font" v-model="registerTagVisible" title="新建标签" :width="300"
             @ok="handleRegisterTagOk" @cancel="handleRegisterTagCancel">
      <a-input v-model="newTagName" placeholder="新的标签名称"></a-input>
    </a-modal>

    <a-modal class="modal-font" v-model="registerGroupVisible" title="新建菜品组" :width="300"
             @ok="handleRegisterGroupOk" @cancel="handleRegisterGroupCancel">
      <a-input v-model="newGroupName" placeholder="新的菜品组名称"></a-input>
    </a-modal>

    <a-modal class="modal-font" v-model="addInventoryVisible" title="添加库存" :width="300"
             @ok="handleAddInventoryOk" @cancel="handleAddInventoryCancel">
      <a-input v-model="inventoryAddition" placeholder="添加的库存量"></a-input>
    </a-modal>

    <a-modal class="modal-font" v-model="addTagVisible" title="添加标签"
             @ok="handleAddTag2DishOk" @cancel="handleAddTag2DishCancel">
      <a-checkbox-group v-model="selectedTags">
        <a-checkbox v-for="tag in allTags" :key="tag.Tid" :value="tag.Tid">
          {{ tag.Tname }}
        </a-checkbox>
      </a-checkbox-group>
    </a-modal>
  </div>


</template>

<script>
import {mapGetters, mapState} from "vuex";
import axios from "axios";
import {message} from "ant-design-vue";

export default {
  data() {
    return {
      dishList: {
        // 1: {
        //   id: 1,
        //   name: "Apple",
        //   pic: "1.jpg",
        //   score: 4.6,
        //   price: 3,
        //   star: 23,
        //   remain: 12,
        //   description: "苹果，又称柰或林檎，是苹果树的果实，一般呈红色，但需视品种而定，富含矿物质和维生素，是人们最常食用的水果之一。" +
        //       "人们根据需求的不同口感、用途（比如烹饪、生吃、酿苹果酒等）培育不同的品种，已知有超过7,500个苹果品种，拥有一系列人们需要的不同特性。",
        //   tags: [
        //     {id: 1, name: '不辣'},
        //     {id: 2, name: '清真'}
        //   ],
        // },
        // 2: {
        //   id: 2,
        //   name: "Orange",
        //   pic: "2.jpg",
        //   score: 4.7,
        //   price: 3,
        //   star: 0,
        //   remain: 100,
        //   description: "null",
        //   tags: [
        //     {id: 1, name: '不辣'},
        //     {id: 3, name: '甜'}
        //   ],
        // },
      },
      searchInput: null,
      tagColors: {},
      // modals
      curDishId: null,

      registerDishVisible: false,
      allGroups: [
        // {Gid: 1, Gname: '主食'},
        // {Gid: 2, Gname: '水果'},
        // {Gid: 3, Gname: '甜点'}
      ],
      newDishName: null,
      newDishPrice: null,
      newDishDescription: null,
      newDishInventory: null,
      newDishPicture: null,
      newDishGid: null,

      registerTagVisible: false,
      newTagName: null,

      registerGroupVisible: false,
      newGroupName: null,

      addInventoryVisible: false,
      inventoryAddition: null,

      addTagVisible: false,
      allTags: [
        // {id: 1, name: '不辣'},
        // {id: 2, name: '清真'},
        // {id: 3, name: '甜'}
      ],
      selectedTags: [],
    }
  },
  created() {
    this.init();
    this.generateRandomColors();
  },
  watch: {
    'dishList'() {
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
        const response = await axios.get('GetDishWithTag/');
        const dishList = {};
        response.data.dishList.forEach((dish) => {
          dishList[dish.Did] = dish;
        })
        this.dishList = dishList;
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async searchDish() {
      try {
        const request = {keyword: this.searchInput};
        const response = await axios.post('SearchDish/', request);
        const dishList = {};
        response.data.forEach((dish) => {
          dishList[dish.id] = dish;
        })
        this.dishList = dishList;
        message.success('search completed');
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async getAllGroups() {
      try {
        const response = await axios.get('GetAllGroup/');
        this.allGroups = response.data.groupList;
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async registerDish() {
      try {
        console.log(this.newDishPicture)
        // message.success("in register")
        const request = new FormData()
        request.append('Dname', this.newDishName);
        request.append('price', this.newDishPrice);
        request.append('remain', this.newDishInventory);
        request.append('description', this.newDishDescription);
        request.append('Gid', this.newDishGid);
        request.append('picture',this.newDishPicture.url);
        // {
        //   Dname: this.newDishName,
        //   price: this.newDishPrice,
        //   remain: this.newDishInventory,
        //   description: this.newDishDescription,
        //   Gid: this.newDishGid,
        //   picture: this.newDishPicture,
        // })
        // message.success("before post")
        const response = await axios.post('AddDish/', request);
        if (!response.data.value) {
          message.success('添加菜品成功！');
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async registerTag() {
      try {
        const request = {Tname: this.newTagName};
        const response = await axios.post('AddTag/', request);
        if (!response.data.value) {
          message.success('添加标签成功！');
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async registerGroup() {
      try {
        const request = {Gname: this.newGroupName};
        const response = await axios.post('AddGroup/', request);
        if (!response.data.value) {
          message.success('添加菜品组成功！');
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async addInventory() {
      try {
        const request = {Did: this.curDishId, number: this.inventoryAddition};
        const response = await axios.post('AddDishRemain/', request);
        if (!response.data.value) {
          message.success('添加库存成功！');
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async getAllTags() {
      try {
        const response = await axios.get('GetAllTag/');
        this.allTags = response.data.tagList;
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },
    async addTag2Dish() {
      try {
        const request = {Did: this.curDishId, TidList: this.selectedTags};
        const response = await axios.post('AddDishTag/', request);
        if (!response.data.value) {
          message.success('添加标签成功！');
        } else {
          message.error(response.data.message);
        }
      } catch (error) {
        message.error('Error loading data from the database:', error);
      }
    },

    // tag colors
    randomColor() {
      const randomComponent = () => Math.floor(Math.random() * 200);
      return `rgb(${randomComponent()}, ${randomComponent()}, ${randomComponent()})`;
    },
    generateRandomColors() {
      const colors = {};
      Object.values(this.dishList).forEach((dish) => {
        dish.tags.forEach((tag) => {
          if (!Object.prototype.hasOwnProperty.call(colors, tag.id)) {
            colors[tag.id] = this.randomColor();
          }
        })
      })
      this.tagColors = colors;
    },


    handelSearch() {
      this.searchDish();
      this.searchInput = null;
    },

    /*-------- register new dish ----------*/
    handleRegisterDish() {
      this.getAllGroups();
      this.registerDishVisible = true;
    },
    beforeUploadDishPicture(file) {
      // console.log('File:', file); // 输出看看 file 是什么
      // if (file) {
      //   this.newDishPicture = file
      //   console.log('Pic:', this.newDishPicture)
      //   message.success('before upload');
      // } else {
      //   // 处理文件不存在的情况
      //   console.error('No file selected');
      //   // 在这里可以添加一些用户友好的提示
      // }
      const reader = new FileReader();
      reader.onload = (e) => {
        this.newDishPicture = ({id: Date.now(), url: e.target.result});
      };
      reader.readAsDataURL(file);
      return true;
    },
    handleRegisterDishOk() {
      if (!this.newDishName || !this.newDishPrice || !this.newDishInventory || !this.newDishDescription) {
        message.error('请输入完整信息！');
        return;
      } else if (!this.newDishGid) {
        message.error('请选择菜品组！');
        return;
      } else if (!this.newDishPicture) {
        message.error('请上传菜品图片！');
        return;
      }
      this.registerDish();
      this.registerDishVisible = false;
      setTimeout(() => {
        this.newDishName = null;
        this.newDishPrice = null;
        this.newDishInventory = null;
        this.newDishDescription = null;
        this.newDishGid = null;
        this.newDishPicture = null;
      }, 300);
    },
    handleRegisterDishCancel() {
      this.registerDishVisible = false;
      setTimeout(() => {
        this.newDishName = null;
        this.newDishPrice = null;
        this.newDishInventory = null;
        this.newDishDescription = null;
        this.newDishGid = null;
        this.newDishPicture = null;
      }, 300);
    },
    /*-------- register new group ----------*/
    handleRegisterGroup() {
      this.registerGroupVisible = true;
    },
    handleRegisterGroupOk() {
      if (!this.newGroupName) {
        message.error('请输入标签名称！');
        return;
      }
      this.registerGroup();
      this.registerGroupVisible = false;
      setTimeout(() => {
        this.newGroupName = null;
      }, 300);
    },
    handleRegisterGroupCancel() {
      this.registerGroupVisible = false;
      setTimeout(() => {
        this.newGroupName = null;
      }, 300);
    },
    /*-------- register new tag ----------*/
    handleRegisterTag() {
      this.registerTagVisible = true;
    },
    handleRegisterTagOk() {
      if (!this.newTagName) {
        message.error('请输入标签名称！');
        return;
      }
      this.registerTag();
      this.registerTagVisible = false;
      setTimeout(() => {
        this.newTagName = null;
      }, 300);
    },
    handleRegisterTagCancel() {
      this.registerTagVisible = false;
      setTimeout(() => {
        this.newTagName = null;
      }, 300);
    },

    /*-------- add inventory ----------*/
    handelAddInventory(dishId) {
      this.curDishId = dishId;
      this.addInventoryVisible = true;
    },
    handleAddInventoryOk() {
      if (!this.inventoryAddition) {
        message.error('请输入添加的库存量！');
        return;
      }
      this.addInventory();
      this.addInventoryVisible = false;
      setTimeout(() => {
        this.inventoryAddition = null;
      }, 300);
    },
    handleAddInventoryCancel() {
      this.addInventoryVisible = false;
      setTimeout(() => {
        this.inventoryAddition = null;
      }, 300);
    },

    /*-------- add tag to dish ----------*/
    handleAddTag2Dish(dishId) {
      this.curDishId = dishId;
      this.getAllTags();
      this.addTagVisible = true;
    },
    handleAddTag2DishOk() {
      if (this.selectedTags.length === 0) {
        message.error('请选择标签！');
        return;
      }
      this.addTag2Dish();
      this.addTagVisible = false;
      setTimeout(() => {
        this.selectedTags = [];
      }, 300);
    },
    handleAddTag2DishCancel() {
      this.addTagVisible = false;
      setTimeout(() => {
        this.selectedTags = [];
      }, 300);
    },
  }
}

</script>
<style scoped lang="less">
.new-page {
  height: 100%;
  background-color: @base-bg-color;
  padding: 20px;
  border-radius: 4px;
  font-family: "Times New Roman", fangsong;
}

.dish-table-row {
  padding: 20px;
  font-weight: bolder;
  border-bottom: #e6e6e0 1px solid;
}

.dish-table-row .ant-col {
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-tag {
  display: inline-block;
  font-size: 10px;
  padding: 4px 10px;
  border-radius: 40px;
  margin-left: 10px;
}

.modal-font {
  font-family: "Times New Roman", fangsong;
}
</style>