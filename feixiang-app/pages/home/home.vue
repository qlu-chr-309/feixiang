<template>
  <view class="home-container">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <view class="search-input-wrap">
        <text class="iconfont icon-search"></text>
        <input class="search-input" type="text" placeholder="搜索无人机设备、服务" confirm-type="search" @confirm="handleSearch" />
      </view>
    </view>
    
    <!-- 轮播图 -->
    <swiper class="banner" indicator-dots autoplay circular>
      <swiper-item v-for="(item, index) in banners" :key="index">
        <image class="banner-image" :src="item.image" mode="aspectFill" @click="handleBannerClick(item)"></image>
      </swiper-item>
    </swiper>
    
    <!-- 功能模块 -->
    <view class="function-grid">
      <view class="function-item" @click="navigate('/pages/demand/demand')">
        <image class="function-icon" src="/static/icons/demand-icon.png" mode="aspectFit"></image>
        <text class="function-text">下单选择用途</text>
      </view>
      <view class="function-item" @click="navigate('/pages/service/service?type=rent')">
        <image class="function-icon" src="/static/icons/rent-icon.png" mode="aspectFit"></image>
        <text class="function-text">租赁无人机</text>
      </view>
      <view class="function-item" @click="navigate('/pages/service/service?type=upgrade')">
        <image class="function-icon" src="/static/icons/upgrade-icon.png" mode="aspectFit"></image>
        <text class="function-text">装备升级</text>
      </view>
      <view class="function-item" @click="navigate('/pages/service/service?type=ar')">
        <image class="function-icon" src="/static/icons/ar-icon.png" mode="aspectFit"></image>
        <text class="function-text">AR虚拟飞行</text>
      </view>
      <view class="function-item" @click="navigate('/pages/service/service?type=competition')">
        <image class="function-icon" src="/static/icons/competition-icon.png" mode="aspectFit"></image>
        <text class="function-text">线上竞技</text>
      </view>
      <view class="function-item" @click="navigate('/pages/service/service?type=innovation')">
        <image class="function-icon" src="/static/icons/innovation-icon.png" mode="aspectFit"></image>
        <text class="function-text">创客中心</text>
      </view>
      <view class="function-item" @click="navigate('/pages/service/service?type=training')">
        <image class="function-icon" src="/static/icons/training-icon.png" mode="aspectFit"></image>
        <text class="function-text">培训服务</text>
      </view>
      <view class="function-item" @click="navigate('/pages/news/news')">
        <image class="function-icon" src="/static/icons/news-icon.png" mode="aspectFit"></image>
        <text class="function-text">行业资讯</text>
      </view>
    </view>
    
    <!-- 推荐产品 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">热门设备</text>
        <text class="section-more" @click="navigate('/pages/product/list')">查看更多</text>
      </view>
      <scroll-view class="product-scroll" scroll-x>
        <view class="product-card" v-for="(item, index) in products" :key="index" @click="navigateToProduct(item.id)">
          <image class="product-image" :src="item.image" mode="aspectFill"></image>
          <view class="product-info">
            <text class="product-name">{{item.name}}</text>
            <text class="product-price">¥{{item.price}}</text>
          </view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 服务推荐 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">推荐服务</text>
        <text class="section-more" @click="navigate('/pages/service/list')">查看更多</text>
      </view>
      <view class="service-grid">
        <view class="service-card" v-for="(item, index) in services" :key="index" @click="navigateToService(item.id)">
          <image class="service-image" :src="item.image" mode="aspectFill"></image>
          <view class="service-info">
            <text class="service-name">{{item.name}}</text>
            <text class="service-desc">{{item.description}}</text>
            <text class="service-price">¥{{item.price}}/{{item.unit}}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      banners: [
        { image: '/static/images/banner1.jpg', url: '/pages/activity/detail?id=1' },
        { image: '/static/images/banner2.jpg', url: '/pages/product/detail?id=2' },
        { image: '/static/images/banner3.jpg', url: '/pages/service/detail?id=3' }
      ],
      products: [
        { id: 1, name: 'DJI Mini 3 Pro', price: '3999', image: '/static/images/product1.jpg' },
        { id: 2, name: 'DJI Air 2S', price: '5999', image: '/static/images/product2.jpg' },
        { id: 3, name: 'DJI Mavic 3', price: '12999', image: '/static/images/product3.jpg' },
        { id: 4, name: 'FIMI X8 SE', price: '2999', image: '/static/images/product4.jpg' }
      ],
      services: [
        { id: 1, name: '城市航拍服务', description: '专业航拍团队，高清成片', price: '1500', unit: '次', image: '/static/images/service1.jpg' },
        { id: 2, name: '农业植保服务', description: '高效精准植保作业', price: '200', unit: '亩', image: '/static/images/service2.jpg' }
      ]
    }
  },
  onLoad() {
    // 加载首页数据
    this.loadHomeData();
  },
  methods: {
    loadHomeData() {
      // 模拟从后端加载数据
      console.log('加载首页数据');
      
      // 实际项目中应该调用API获取数据
      // this.$request({
      //   url: '/home/data',
      //   method: 'GET'
      // }).then(res => {
      //   this.banners = res.banners;
      //   this.products = res.products;
      //   this.services = res.services;
      // }).catch(err => {
      //   console.error('加载首页数据失败', err);
      // });
    },
    handleSearch(e) {
      const keyword = e.detail.value;
      uni.navigateTo({
        url: `/pages/search/search?keyword=${keyword}`
      });
    },
    handleBannerClick(item) {
      uni.navigateTo({
        url: item.url
      });
    },
    navigate(url) {
      if (url.startsWith('/pages/')) {
        if (url.indexOf('?') > -1) {
          const baseUrl = url.split('?')[0];
          const params = url.split('?')[1];
          
          // 判断是否是 tabBar 页面
          if (['pages/home/home', 'pages/demand/demand', 'pages/service/service', 'pages/community/community', 'pages/personal/personal'].includes(baseUrl.slice(1))) {
            uni.switchTab({
              url: baseUrl
            });
          } else {
            uni.navigateTo({
              url: url
            });
          }
        } else {
          // 判断是否是 tabBar 页面
          if (['pages/home/home', 'pages/demand/demand', 'pages/service/service', 'pages/community/community', 'pages/personal/personal'].includes(url.slice(1))) {
            uni.switchTab({
              url: url
            });
          } else {
            uni.navigateTo({
              url: url
            });
          }
        }
      }
    },
    navigateToProduct(id) {
      uni.navigateTo({
        url: `/pages/product/detail?id=${id}`
      });
    },
    navigateToService(id) {
      uni.navigateTo({
        url: `/pages/service/detail?id=${id}`
      });
    }
  },
  onPullDownRefresh() {
    // 下拉刷新
    this.loadHomeData();
    setTimeout(() => {
      uni.stopPullDownRefresh();
    }, 1000);
  }
}
</script>

<style>
.home-container {
  background-color: #f8f8f8;
  min-height: 100vh;
}

/* 搜索栏 */
.search-bar {
  background-color: #fff;
  padding: 20rpx 30rpx;
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

.icon-search {
  font-size: 32rpx;
  color: #999;
  margin-right: 10rpx;
}

.search-input {
  flex: 1;
  height: 70rpx;
  font-size: 28rpx;
}

/* 轮播图 */
.banner {
  height: 300rpx;
  margin-bottom: 20rpx;
}

.banner-image {
  width: 100%;
  height: 100%;
}

/* 功能模块 */
.function-grid {
  display: flex;
  flex-wrap: wrap;
  background-color: #fff;
  padding: 20rpx 10rpx;
  margin-bottom: 20rpx;
}

.function-item {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx 0;
}

.function-icon {
  width: 80rpx;
  height: 80rpx;
  margin-bottom: 10rpx;
}

.function-text {
  font-size: 24rpx;
  color: #333;
}

/* 公共部分 */
.section {
  background-color: #fff;
  margin-bottom: 20rpx;
  padding: 20rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  position: relative;
  padding-left: 20rpx;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 6rpx;
  height: 30rpx;
  width: 6rpx;
  background-color: #007AFF;
  border-radius: 3rpx;
}

.section-more {
  font-size: 26rpx;
  color: #666;
}

/* 产品推荐 */
.product-scroll {
  white-space: nowrap;
}

.product-card {
  display: inline-block;
  width: 240rpx;
  margin-right: 20rpx;
  border-radius: 12rpx;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.1);
}

.product-image {
  width: 240rpx;
  height: 240rpx;
}

.product-info {
  padding: 16rpx;
}

.product-name {
  font-size: 26rpx;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.product-price {
  font-size: 26rpx;
  color: #ff4500;
  margin-top: 6rpx;
  display: block;
}

/* 服务推荐 */
.service-grid {
  display: flex;
  flex-direction: column;
}

.service-card {
  display: flex;
  margin-bottom: 20rpx;
  background-color: #fff;
  border-radius: 12rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.1);
}

.service-image {
  width: 200rpx;
  height: 160rpx;
}

.service-info {
  flex: 1;
  padding: 16rpx;
}

.service-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
  display: block;
}

.service-desc {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 16rpx;
  display: block;
}

.service-price {
  font-size: 26rpx;
  color: #ff4500;
  display: block;
}
</style> 