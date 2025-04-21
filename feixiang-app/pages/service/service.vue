<template>
  <view class="service-container">
    <!-- 服务类型选择 -->
    <view class="service-types">
      <scroll-view scroll-x class="type-scroll">
        <view 
          class="type-item" 
          :class="{ active: activeType === type.id }" 
          v-for="type in serviceTypes" 
          :key="type.id"
          @click="selectType(type.id)"
        >
          <text>{{ type.name }}</text>
        </view>
      </scroll-view>
    </view>
    
    <!-- 搜索栏 -->
    <view class="search-bar">
      <view class="search-input-wrap">
        <text class="iconfont icon-search"></text>
        <input class="search-input" type="text" placeholder="搜索服务" confirm-type="search" @confirm="handleSearch" />
      </view>
    </view>
    
    <!-- 筛选条件 -->
    <view class="filter-bar">
      <view class="filter-item" @click="toggleFilter('region')">
        <text>地区</text>
        <text class="iconfont icon-down"></text>
      </view>
      <view class="filter-item" @click="toggleFilter('sort')">
        <text>排序</text>
        <text class="iconfont icon-down"></text>
      </view>
      <view class="filter-item" @click="toggleFilter('price')">
        <text>价格</text>
        <text class="iconfont icon-down"></text>
      </view>
      <view class="filter-item" @click="toggleFilter('more')">
        <text>更多</text>
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
      </view>
      
      <!-- 价格筛选 -->
      <view v-if="activeFilter === 'price'" class="price-filter">
        <view 
          class="price-item" 
          :class="{ active: priceRange === range.id }" 
          v-for="range in priceRanges" 
          :key="range.id"
          @click="selectPrice(range.id)"
        >
          <text>{{ range.name }}</text>
        </view>
      </view>
      
      <!-- 更多筛选 -->
      <view v-if="activeFilter === 'more'" class="more-filter">
        <view class="filter-group">
          <view class="filter-title">服务评分</view>
          <view class="tag-list">
            <view 
              class="tag-item" 
              :class="{ active: selectedRating === rating.id }" 
              v-for="rating in ratings" 
              :key="rating.id"
              @click="selectRating(rating.id)"
            >
              <text>{{ rating.name }}</text>
            </view>
          </view>
        </view>
        
        <view class="filter-group">
          <view class="filter-title">服务特色</view>
          <view class="tag-list">
            <view 
              class="tag-item" 
              :class="{ active: selectedFeatures.includes(feature.id) }" 
              v-for="feature in features" 
              :key="feature.id"
              @click="toggleFeature(feature.id)"
            >
              <text>{{ feature.name }}</text>
            </view>
          </view>
        </view>
        
        <view class="filter-buttons">
          <button class="reset-btn" @click="resetFilter">重置</button>
          <button class="apply-btn" @click="applyFilter">确定</button>
        </view>
      </view>
    </view>
    
    <!-- 服务列表 -->
    <view class="service-list" v-if="serviceList.length > 0">
      <view class="service-card" v-for="(item, index) in serviceList" :key="index" @click="navigateToDetail(item.id)">
        <image class="service-image" :src="item.image" mode="aspectFill"></image>
        <view class="service-info">
          <view class="service-title">{{ item.title }}</view>
          <view class="service-tags">
            <text class="service-tag" v-for="(tag, tagIndex) in item.tags" :key="tagIndex">{{ tag }}</text>
          </view>
          <view class="service-provider">
            <image class="provider-avatar" :src="item.providerAvatar"></image>
            <text class="provider-name">{{ item.providerName }}</text>
            <text class="provider-rating">{{ item.rating }}分</text>
          </view>
          <view class="service-bottom">
            <text class="service-price">¥{{ item.price }}</text>
            <text class="service-orders">已接单{{ item.orderCount }}次</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 空状态 -->
    <view class="empty-state" v-else>
      <image class="empty-image" src="/static/images/empty.png" mode="aspectFit"></image>
      <text class="empty-text">暂无相关服务</text>
    </view>
    
    <!-- 悬浮发布按钮 -->
    <view class="floating-button" @click="navigateToPublish">
      <text class="button-icon">+</text>
      <text class="button-text">发布需求</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 当前选中的服务类型
      activeType: 'all',
      // 服务类型列表
      serviceTypes: [
        { id: 'all', name: '全部' },
        { id: 'ar', name: 'AR虚拟飞行' },
        { id: 'competition', name: '线上竞技' },
        { id: 'innovation', name: '创客中心' },
        { id: 'training', name: '培训服务' },
        { id: 'rental', name: '无人机租赁' },
        { id: 'upgrade', name: '设备升级' }
      ],
      
      // 筛选相关
      activeFilter: '', // 当前打开的筛选面板
      selectedRegion: 'all',
      sortType: 'default',
      priceRange: 'all',
      selectedRating: 'all',
      selectedFeatures: [],
      
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
      sortTypes: [
        { id: 'default', name: '默认排序' },
        { id: 'price_asc', name: '价格从低到高' },
        { id: 'price_desc', name: '价格从高到低' },
        { id: 'rating', name: '评分优先' },
        { id: 'orders', name: '接单量优先' }
      ],
      priceRanges: [
        { id: 'all', name: '全部价格' },
        { id: 'under_1000', name: '1000元以下' },
        { id: '1000_3000', name: '1000-3000元' },
        { id: '3000_5000', name: '3000-5000元' },
        { id: 'above_5000', name: '5000元以上' }
      ],
      ratings: [
        { id: 'all', name: '全部' },
        { id: '4.5', name: '4.5分以上' },
        { id: '4.0', name: '4.0分以上' },
        { id: '3.5', name: '3.5分以上' }
      ],
      features: [
        { id: 'certification', name: '持证飞手' },
        { id: 'insurance', name: '保险保障' },
        { id: 'equipment', name: '设备齐全' },
        { id: '24h', name: '24小时服务' },
        { id: 'free_quote', name: '免费报价' },
        { id: 'experience', name: '经验丰富' }
      ],
      
      // 服务列表
      serviceList: [
        {
          id: 1,
          title: '专业航拍服务，高清影像定制',
          tags: ['持证飞手', '设备齐全'],
          providerName: '天空影像工作室',
          providerAvatar: '/static/images/avatar1.jpg',
          rating: 4.8,
          price: '1200',
          orderCount: 156,
          image: '/static/images/service1.jpg'
        },
        {
          id: 2,
          title: '农田植保无人机服务，高效省心',
          tags: ['保险保障', '经验丰富'],
          providerName: '绿农植保科技',
          providerAvatar: '/static/images/avatar2.jpg',
          rating: 4.6,
          price: '200',
          orderCount: 322,
          image: '/static/images/service2.jpg'
        },
        {
          id: 3,
          title: '工业巡检无人机服务，安全可靠',
          tags: ['持证飞手', '24小时服务'],
          providerName: '慧眼巡检科技',
          providerAvatar: '/static/images/avatar3.jpg',
          rating: 4.9,
          price: '3000',
          orderCount: 87,
          image: '/static/images/service3.jpg'
        }
      ]
    }
  },
  onLoad(options) {
    // 如果有类型参数，切换到对应类型
    if (options.type) {
      this.activeType = options.type;
    }
    
    // 加载服务列表
    this.loadServiceList();
  },
  methods: {
    // 加载服务列表
    loadServiceList() {
      // 模拟请求服务端数据
      // 实际项目中应该调用API
      console.log('加载服务列表, 类型:', this.activeType);
    },
    
    // 选择服务类型
    selectType(typeId) {
      this.activeType = typeId;
      this.activeFilter = ''; // 关闭筛选面板
      this.loadServiceList();
    },
    
    // 搜索
    handleSearch(e) {
      const keyword = e.detail.value;
      console.log('搜索关键词:', keyword);
      // 搜索操作
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
    
    selectSort(sortId) {
      this.sortType = sortId;
      this.activeFilter = ''; // 选择后关闭面板
      this.loadServiceList(); // 重新加载列表
    },
    
    selectPrice(priceId) {
      this.priceRange = priceId;
      this.activeFilter = ''; // 选择后关闭面板
      this.loadServiceList(); // 重新加载列表
    },
    
    selectRating(ratingId) {
      this.selectedRating = ratingId;
    },
    
    toggleFeature(featureId) {
      if (this.selectedFeatures.includes(featureId)) {
        this.selectedFeatures = this.selectedFeatures.filter(id => id !== featureId);
      } else {
        this.selectedFeatures.push(featureId);
      }
    },
    
    resetFilter() {
      this.selectedRating = 'all';
      this.selectedFeatures = [];
    },
    
    applyFilter() {
      this.activeFilter = ''; // 关闭筛选面板
      this.loadServiceList(); // 重新加载列表
    },
    
    // 导航到服务详情
    navigateToDetail(id) {
      uni.navigateTo({
        url: `/pages/service/detail?id=${id}`
      });
    },
    
    // 导航到发布需求页面
    navigateToPublish() {
      uni.switchTab({
        url: '/pages/demand/demand'
      });
    }
  }
}
</script>

<style>
.service-container {
  background-color: #f8f8f8;
  min-height: 100vh;
}

/* 服务类型选择 */
.service-types {
  background-color: #fff;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #eee;
  position: sticky;
  top: 0;
  z-index: 100;
}

.type-scroll {
  white-space: nowrap;
}

.type-item {
  display: inline-block;
  padding: 10rpx 30rpx;
  margin: 0 10rpx;
  font-size: 28rpx;
  color: #666;
  position: relative;
}

.type-item.active {
  color: #007AFF;
  font-weight: 500;
}

.type-item.active::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -10rpx;
  transform: translateX(-50%);
  width: 40rpx;
  height: 4rpx;
  background-color: #007AFF;
  border-radius: 2rpx;
}

/* 搜索栏 */
.search-bar {
  padding: 20rpx;
  background-color: #fff;
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

.region-list, .sort-filter, .price-filter {
  display: flex;
  flex-wrap: wrap;
}

.region-item, .sort-item, .price-item {
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

.region-item.active, .sort-item.active, .price-item.active, .tag-item.active {
  background-color: #e6f2ff;
  color: #007AFF;
}

.filter-group {
  margin-bottom: 30rpx;
}

.filter-title {
  font-size: 28rpx;
  font-weight: 500;
  margin-bottom: 20rpx;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
}

.tag-item {
  padding: 10rpx 20rpx;
  background-color: #f5f5f5;
  border-radius: 6rpx;
  margin: 10rpx;
  font-size: 26rpx;
}

.filter-buttons {
  display: flex;
  margin-top: 30rpx;
}

.reset-btn, .apply-btn {
  flex: 1;
  height: 80rpx;
  line-height: 80rpx;
  text-align: center;
  border-radius: 6rpx;
  font-size: 28rpx;
}

.reset-btn {
  background-color: #f5f5f5;
  color: #666;
  margin-right: 20rpx;
}

.apply-btn {
  background-color: #007AFF;
  color: #fff;
}

/* 服务列表 */
.service-list {
  padding: 20rpx;
}

.service-card {
  display: flex;
  background-color: #fff;
  border-radius: 12rpx;
  margin-bottom: 20rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.05);
}

.service-image {
  width: 220rpx;
  height: 220rpx;
}

.service-info {
  flex: 1;
  padding: 20rpx;
  display: flex;
  flex-direction: column;
}

.service-title {
  font-size: 28rpx;
  font-weight: 500;
  margin-bottom: 10rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.service-tags {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 10rpx;
}

.service-tag {
  font-size: 22rpx;
  color: #007AFF;
  background-color: #e6f2ff;
  padding: 4rpx 12rpx;
  border-radius: 4rpx;
  margin-right: 10rpx;
  margin-bottom: 10rpx;
}

.service-provider {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
}

.provider-avatar {
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  margin-right: 10rpx;
}

.provider-name {
  font-size: 24rpx;
  color: #666;
  margin-right: 20rpx;
}

.provider-rating {
  font-size: 24rpx;
  color: #ff9500;
}

.service-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.service-price {
  font-size: 32rpx;
  color: #ff4500;
  font-weight: 500;
}

.service-orders {
  font-size: 24rpx;
  color: #999;
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
}

/* 悬浮按钮 */
.floating-button {
  position: fixed;
  right: 30rpx;
  bottom: 100rpx;
  background-color: #007AFF;
  color: #fff;
  display: flex;
  align-items: center;
  padding: 20rpx 30rpx;
  border-radius: 40rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 122, 255, 0.4);
  z-index: 100;
}

.button-icon {
  font-size: 36rpx;
  margin-right: 10rpx;
}

.button-text {
  font-size: 28rpx;
}
</style> 