<template>
  <view class="supplier-container">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <view class="search-input-wrap">
        <text class="iconfont icon-search"></text>
        <input class="search-input" type="text" placeholder="搜索服务商" confirm-type="search" @confirm="handleSearch" />
      </view>
    </view>
    
    <!-- 筛选条件 -->
    <view class="filter-bar">
      <view class="filter-item" @click="toggleFilter('region')">
        <text>地区</text>
        <text class="iconfont icon-down"></text>
      </view>
      <view class="filter-item" @click="toggleFilter('category')">
        <text>类型</text>
        <text class="iconfont icon-down"></text>
      </view>
      <view class="filter-item" @click="toggleFilter('sort')">
        <text>排序</text>
        <text class="iconfont icon-down"></text>
      </view>
    </view>
    
    <!-- 筛选面板 -->
    <view class="filter-panel" v-if="activeFilter">
      <!-- 地区筛选 -->
      <view v-if="activeFilter === 'region'" class="region-filter">
        <view class="region-list">
          <view 
            class="region-item" 
            :class="{ active: selectedRegion === region.id }" 
            v-for="region in regions" 
            :key="region.id"
            @click="selectRegion(region.id)"
          >
            <text>{{ region.name }}</text>
          </view>
        </view>
        <button class="confirm-btn" @click="confirmFilter">确定</button>
      </view>
      
      <!-- 类型筛选 -->
      <view v-if="activeFilter === 'category'" class="category-filter">
        <view 
          class="category-item" 
          :class="{ active: selectedCategory === category.id }" 
          v-for="category in categories" 
          :key="category.id"
          @click="selectCategory(category.id)"
        >
          <text>{{ category.name }}</text>
        </view>
        <button class="confirm-btn" @click="confirmFilter">确定</button>
      </view>
      
      <!-- 排序筛选 -->
      <view v-if="activeFilter === 'sort'" class="sort-filter">
        <view 
          class="sort-item" 
          :class="{ active: sortType === type.id }" 
          v-for="type in sortTypes" 
          :key="type.id"
          @click="selectSort(type.id)"
        >
          <text>{{ type.name }}</text>
        </view>
        <button class="confirm-btn" @click="confirmFilter">确定</button>
      </view>
    </view>
    
    <!-- 供应商列表 -->
    <view class="supplier-list">
      <view class="supplier-card" v-for="(item, index) in supplierList" :key="index" @click="navigateToDetail(item.id)">
        <view class="supplier-header">
          <image class="supplier-logo" :src="item.logo" mode="aspectFill"></image>
          <view class="supplier-info">
            <view class="supplier-name">{{ item.name }}</view>
            <view class="supplier-type">{{ item.type }}</view>
            <view class="supplier-rating">
              <text class="rating-score">{{ item.rating }}</text>
              <view class="rating-stars">
                <text class="star" v-for="i in 5" :key="i" :class="{ active: i <= Math.floor(item.rating) }">★</text>
              </view>
              <text class="review-count">({{ item.reviewCount }})</text>
            </view>
          </view>
        </view>
        
        <view class="supplier-tags">
          <text class="tag" v-for="(tag, tagIndex) in item.tags" :key="tagIndex">{{ tag }}</text>
        </view>
        
        <view class="supplier-services">
          <text class="service-title">主营服务：</text>
          <text class="service-list">{{ item.services.join('、') }}</text>
        </view>
        
        <view class="supplier-footer">
          <text class="location">{{ item.location }}</text>
          <view class="action-btns">
            <button class="btn btn-contact" @click.stop="contactSupplier(item)">联系</button>
            <button class="btn btn-view" @click.stop="navigateToDetail(item.id)">查看</button>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 加载更多 -->
    <view class="load-more" v-if="supplierList.length > 0">
      <text v-if="isLoading">正在加载...</text>
      <text v-else-if="hasMore">点击加载更多</text>
      <text v-else>没有更多了</text>
    </view>
    
    <!-- 空状态 -->
    <view class="empty-state" v-if="supplierList.length === 0">
      <image class="empty-image" src="/static/images/empty.png" mode="aspectFit"></image>
      <text class="empty-text">暂无服务商信息</text>
      <button class="refresh-btn" @click="loadSupplierList">刷新</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 筛选相关
      activeFilter: '', // 当前打开的筛选面板
      selectedRegion: 'all',
      selectedCategory: 'all',
      sortType: 'default',
      
      // 筛选选项
      regions: [
        { id: 'all', name: '全部地区' },
        { id: 'bj', name: '北京' },
        { id: 'sh', name: '上海' },
        { id: 'gz', name: '广州' },
        { id: 'sz', name: '深圳' },
        { id: 'cd', name: '成都' },
        { id: 'hz', name: '杭州' }
      ],
      categories: [
        { id: 'all', name: '全部类型' },
        { id: 'aerial', name: '航拍服务' },
        { id: 'plant', name: '植保服务' },
        { id: 'inspection', name: '巡检服务' },
        { id: 'modeling', name: '建模服务' },
        { id: 'training', name: '培训服务' },
        { id: 'rental', name: '设备租赁' }
      ],
      sortTypes: [
        { id: 'default', name: '默认排序' },
        { id: 'rating_high', name: '评分从高到低' },
        { id: 'rating_low', name: '评分从低到高' },
        { id: 'orders_high', name: '订单量从高到低' },
        { id: 'orders_low', name: '订单量从低到高' }
      ],
      
      // 供应商列表
      supplierList: [
        {
          id: 1,
          name: '天空影像工作室',
          type: '航拍服务商',
          logo: '/static/images/supplier1.jpg',
          rating: 4.8,
          reviewCount: 124,
          tags: ['持证飞手', '设备齐全', '高清成片'],
          services: ['广告航拍', '婚礼跟拍', '活动直播'],
          location: '北京市朝阳区',
          contactPhone: '13800138000'
        },
        {
          id: 2,
          name: '绿农植保科技',
          type: '植保服务商',
          logo: '/static/images/supplier2.jpg',
          rating: 4.6,
          reviewCount: 98,
          tags: ['专业团队', '服务保障', '定期培训'],
          services: ['农田喷洒', '果园防护', '林地防治'],
          location: '广州市番禺区',
          contactPhone: '13900139000'
        },
        {
          id: 3,
          name: '慧眼巡检科技',
          type: '巡检服务商',
          logo: '/static/images/supplier3.jpg',
          rating: 4.9,
          reviewCount: 75,
          tags: ['高精设备', '数据分析', '实时报告'],
          services: ['电力巡检', '管道检测', '光伏巡检'],
          location: '上海市浦东新区',
          contactPhone: '13700137000'
        }
      ],
      
      // 分页加载
      page: 1,
      pageSize: 10,
      hasMore: true,
      isLoading: false
    }
  },
  onLoad() {
    // 加载供应商列表
    this.loadSupplierList();
  },
  methods: {
    // 加载供应商列表
    loadSupplierList() {
      // 模拟请求服务端数据
      // 实际项目中应该调用API
      this.isLoading = true;
      
      setTimeout(() => {
        this.isLoading = false;
        
        // 如果是第一页，直接赋值
        if (this.page === 1) {
          // 数据已经在data中预设了，这里不做处理
        } else {
          // 模拟加载更多数据
          if (this.page <= 3) {
            // 添加更多数据
            const moreData = [
              {
                id: 3 + this.page,
                name: '新航科技有限公司',
                type: '综合服务商',
                logo: '/static/images/supplier4.jpg',
                rating: 4.5,
                reviewCount: 65,
                tags: ['全场景服务', '专业团队', '售后保障'],
                services: ['设备销售', '培训服务', '航拍服务'],
                location: '深圳市南山区',
                contactPhone: '13600136000'
              }
            ];
            this.supplierList = [...this.supplierList, ...moreData];
          } else {
            // 没有更多数据了
            this.hasMore = false;
          }
        }
        
        // 页码增加
        this.page++;
      }, 1000);
    },
    
    // 搜索
    handleSearch(e) {
      const keyword = e.detail.value;
      console.log('搜索关键词:', keyword);
      // 搜索操作
      
      // 重置页码和列表
      this.page = 1;
      this.hasMore = true;
      this.supplierList = [];
      this.loadSupplierList();
    },
    
    // 筛选相关
    toggleFilter(type) {
      if (this.activeFilter === type) {
        this.activeFilter = '';
      } else {
        this.activeFilter = type;
      }
    },
    
    selectRegion(regionId) {
      this.selectedRegion = regionId;
    },
    
    selectCategory(categoryId) {
      this.selectedCategory = categoryId;
    },
    
    selectSort(sortId) {
      this.sortType = sortId;
    },
    
    confirmFilter() {
      this.activeFilter = '';
      
      // 重置页码和列表
      this.page = 1;
      this.hasMore = true;
      this.supplierList = [];
      this.loadSupplierList();
    },
    
    // 导航到供应商详情
    navigateToDetail(id) {
      uni.navigateTo({
        url: `/pages/enterprise/detail?id=${id}`
      });
    },
    
    // 联系供应商
    contactSupplier(supplier) {
      uni.makePhoneCall({
        phoneNumber: supplier.contactPhone,
        success: () => {
          console.log('拨打电话成功');
        },
        fail: (err) => {
          console.error('拨打电话失败', err);
          uni.showToast({
            title: '拨打电话失败',
            icon: 'none'
          });
        }
      });
    },
    
    // 下拉刷新
    onPullDownRefresh() {
      // 重置页码和列表
      this.page = 1;
      this.hasMore = true;
      this.supplierList = [];
      this.loadSupplierList();
      
      setTimeout(() => {
        uni.stopPullDownRefresh();
      }, 1000);
    },
    
    // 触底加载更多
    onReachBottom() {
      if (this.hasMore && !this.isLoading) {
        this.loadSupplierList();
      }
    }
  }
}
</script>

<style>
.supplier-container {
  background-color: #f8f8f8;
  min-height: 100vh;
  padding-bottom: 30rpx;
}

/* 搜索栏 */
.search-bar {
  padding: 20rpx;
  background-color: #fff;
  position: sticky;
  top: 0;
  z-index: 100;
}

.search-input-wrap {
  display: flex;
  align-items: center;
  height: 70rpx;
  background-color: #f5f5f5;
  border-radius: 35rpx;
  padding: 0 30rpx;
}

.search-input {
  flex: 1;
  height: 70rpx;
  font-size: 28rpx;
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  background-color: #fff;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #eee;
}

.filter-item {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 26rpx;
  color: #666;
}

.filter-item text {
  margin-right: 6rpx;
}

/* 筛选面板 */
.filter-panel {
  background-color: #fff;
  padding: 20rpx;
  border-bottom: 1rpx solid #eee;
  animation: slideDown 0.3s;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.region-list, .category-filter, .sort-filter {
  display: flex;
  flex-wrap: wrap;
  padding-bottom: 20rpx;
}

.region-item, .category-item, .sort-item {
  width: calc(33.33% - 20rpx);
  height: 70rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10rpx;
  background-color: #f5f5f5;
  border-radius: 6rpx;
  font-size: 26rpx;
  color: #333;
}

.region-item.active, .category-item.active, .sort-item.active {
  background-color: #e6f2ff;
  color: #007AFF;
}

.confirm-btn {
  width: 100%;
  height: 80rpx;
  line-height: 80rpx;
  text-align: center;
  background-color: #007AFF;
  color: #fff;
  border-radius: 6rpx;
  font-size: 28rpx;
  margin-top: 20rpx;
}

/* 供应商列表 */
.supplier-list {
  padding: 20rpx;
}

.supplier-card {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.05);
}

.supplier-header {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.supplier-logo {
  width: 100rpx;
  height: 100rpx;
  border-radius: 8rpx;
  margin-right: 20rpx;
}

.supplier-info {
  flex: 1;
}

.supplier-name {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 6rpx;
}

.supplier-type {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.supplier-rating {
  display: flex;
  align-items: center;
}

.rating-score {
  font-size: 28rpx;
  color: #ff9500;
  font-weight: bold;
  margin-right: 10rpx;
}

.rating-stars {
  display: flex;
}

.star {
  color: #ddd;
  font-size: 24rpx;
  margin-right: 2rpx;
}

.star.active {
  color: #ff9500;
}

.review-count {
  font-size: 24rpx;
  color: #999;
  margin-left: 6rpx;
}

.supplier-tags {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 20rpx;
}

.tag {
  font-size: 24rpx;
  color: #007AFF;
  background-color: #e6f2ff;
  padding: 6rpx 16rpx;
  border-radius: 4rpx;
  margin-right: 15rpx;
  margin-bottom: 10rpx;
}

.supplier-services {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 20rpx;
  display: flex;
}

.service-title {
  color: #333;
  margin-right: 10rpx;
}

.service-list {
  flex: 1;
}

.supplier-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1rpx solid #eee;
  padding-top: 15rpx;
}

.location {
  font-size: 24rpx;
  color: #999;
}

.action-btns {
  display: flex;
}

.btn {
  font-size: 24rpx;
  height: 60rpx;
  line-height: 60rpx;
  padding: 0 30rpx;
  border-radius: 30rpx;
  margin-left: 15rpx;
}

.btn-contact {
  background-color: #fff;
  color: #007AFF;
  border: 1rpx solid #007AFF;
}

.btn-view {
  background-color: #007AFF;
  color: #fff;
}

/* 加载更多 */
.load-more {
  text-align: center;
  padding: 30rpx 0;
  color: #999;
  font-size: 26rpx;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
}

.empty-image {
  width: 200rpx;
  height: 200rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
  margin-bottom: 30rpx;
}

.refresh-btn {
  background-color: #007AFF;
  color: #fff;
  font-size: 28rpx;
  padding: 10rpx 60rpx;
  border-radius: 30rpx;
}
</style> 