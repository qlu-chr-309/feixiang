<template>
  <view class="personal-container">
    <!-- 用户信息卡片 -->
    <view class="user-card">
      <view class="user-info">
        <image class="avatar" :src="userInfo.avatar || '/static/images/default-avatar.png'" @click="changeAvatar"></image>
        <view class="user-details">
          <view class="nickname">{{ userInfo.nickname || '未登录' }}</view>
          <view class="user-type" v-if="userInfo.id">{{ userTypeName }}</view>
          <view class="login-btn" v-else @click="goToLogin">点击登录</view>
        </view>
      </view>
      <view class="user-stats">
        <view class="stat-item" @click="navigateTo('/pages/personal/wallet')">
          <text class="stat-num">{{ userInfo.balance || '0.00' }}</text>
          <text class="stat-label">钱包余额</text>
        </view>
        <view class="stat-item" @click="navigateTo('/pages/personal/equipment')">
          <text class="stat-num">{{ userInfo.equipmentCount || '0' }}</text>
          <text class="stat-label">我的设备</text>
        </view>
        <view class="stat-item" @click="navigateTo('/pages/personal/coupon')">
          <text class="stat-num">{{ userInfo.couponCount || '0' }}</text>
          <text class="stat-label">优惠券</text>
        </view>
      </view>
    </view>
    
    <!-- 我的订单 -->
    <view class="section-card">
      <view class="section-header">
        <text class="section-title">我的订单</text>
        <view class="view-all" @click="navigateTo('/pages/personal/orders')">
          <text>全部订单</text>
          <text class="arrow">></text>
        </view>
      </view>
      <view class="order-icons">
        <view class="order-icon-item" @click="navigateTo('/pages/personal/orders?status=pending')">
          <image class="order-icon" src="/static/images/order-pending.png"></image>
          <text>待支付</text>
          <text class="badge" v-if="orderBadge.pending">{{ orderBadge.pending }}</text>
        </view>
        <view class="order-icon-item" @click="navigateTo('/pages/personal/orders?status=processing')">
          <image class="order-icon" src="/static/images/order-processing.png"></image>
          <text>进行中</text>
          <text class="badge" v-if="orderBadge.processing">{{ orderBadge.processing }}</text>
        </view>
        <view class="order-icon-item" @click="navigateTo('/pages/personal/orders?status=completed')">
          <image class="order-icon" src="/static/images/order-completed.png"></image>
          <text>已完成</text>
        </view>
        <view class="order-icon-item" @click="navigateTo('/pages/personal/orders?status=review')">
          <image class="order-icon" src="/static/images/order-review.png"></image>
          <text>待评价</text>
          <text class="badge" v-if="orderBadge.review">{{ orderBadge.review }}</text>
        </view>
      </view>
    </view>
    
    <!-- 我的服务 -->
    <view class="section-card">
      <view class="section-header">
        <text class="section-title">我的服务</text>
      </view>
      <view class="service-grid">
        <view class="service-item" @click="navigateTo('/pages/personal/equipment')">
          <image class="service-icon" src="/static/images/service-equipment.png"></image>
          <text>我的设备</text>
        </view>
        <view class="service-item" @click="navigateTo('/pages/personal/wallet')">
          <image class="service-icon" src="/static/images/service-wallet.png"></image>
          <text>钱包</text>
        </view>
        <view class="service-item" @click="navigateTo('/pages/personal/service/repair')">
          <image class="service-icon" src="/static/images/service-repair.png"></image>
          <text>设备维修</text>
        </view>
        <view class="service-item" @click="navigateTo('/pages/personal/service/resale')">
          <image class="service-icon" src="/static/images/service-resale.png"></image>
          <text>设备买卖</text>
        </view>
      </view>
    </view>
    
    <!-- 功能列表 -->
    <view class="function-list">
      <view class="function-item" @click="navigateTo('/pages/personal/settings')">
        <text class="function-name">设置</text>
        <text class="arrow">></text>
      </view>
      <view class="function-item" @click="navigateTo('/pages/personal/help')">
        <text class="function-name">帮助与反馈</text>
        <text class="arrow">></text>
      </view>
      <view class="function-item" @click="navigateTo('/pages/personal/about')">
        <text class="function-name">关于飞享</text>
        <text class="arrow">></text>
      </view>
      <view class="function-item" v-if="userInfo.id" @click="logout">
        <text class="function-name logout">退出登录</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      userInfo: {
        id: '',
        nickname: '',
        avatar: '',
        userType: '',
        balance: '',
        equipmentCount: 0,
        couponCount: 0
      },
      
      orderBadge: {
        pending: 0,
        processing: 2,
        review: 1
      }
    }
  },
  computed: {
    userTypeName() {
      if (!this.userInfo.userType) return '';
      
      return this.userInfo.userType === 'personal' ? '个人买家' : '企业买家';
    }
  },
  onShow() {
    // 获取用户信息
    this.getUserInfo();
    
    // 获取订单徽标数量
    this.getOrderBadges();
  },
  methods: {
    // 获取用户信息
    getUserInfo() {
      // 检查是否登录
      const token = uni.getStorageSync('token');
      if (!token) {
        this.userInfo = {
          id: '',
          nickname: '',
          avatar: '',
          userType: '',
          balance: '',
          equipmentCount: 0,
          couponCount: 0
        };
        return;
      }
      
      // 从本地缓存获取用户信息
      const userInfoStr = uni.getStorageSync('userInfo');
      if (userInfoStr) {
        try {
          const userInfo = JSON.parse(userInfoStr);
          this.userInfo = {
            ...userInfo,
            balance: '1280.00',    // 模拟数据
            equipmentCount: 3,     // 模拟数据
            couponCount: 5         // 模拟数据
          };
        } catch (e) {
          console.error('解析用户信息失败', e);
        }
      }
      
      // 实际项目中应该从服务器获取最新的用户信息
      // this.$request({
      //   url: '/user/info',
      //   method: 'GET'
      // }).then(res => {
      //   this.userInfo = res.data;
      //   uni.setStorageSync('userInfo', JSON.stringify(res.data));
      // }).catch(err => {
      //   console.error('获取用户信息失败', err);
      // });
    },
    
    // 获取订单徽标数量
    getOrderBadges() {
      // 实际项目中应该从服务器获取最新的订单徽标数量
      // this.$request({
      //   url: '/order/badges',
      //   method: 'GET'
      // }).then(res => {
      //   this.orderBadge = res.data;
      // }).catch(err => {
      //   console.error('获取订单徽标数量失败', err);
      // });
    },
    
    // 更换头像
    changeAvatar() {
      if (!this.userInfo.id) {
        this.goToLogin();
        return;
      }
      
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          const tempFilePath = res.tempFilePaths[0];
          
          // 显示上传中提示
          uni.showLoading({
            title: '上传中...'
          });
          
          // 模拟上传
          setTimeout(() => {
            uni.hideLoading();
            
            // 更新头像
            this.userInfo.avatar = tempFilePath;
            
            uni.showToast({
              title: '头像更新成功',
              icon: 'success'
            });
          }, 1500);
          
          // 实际项目中应该上传头像到服务器
          // uni.uploadFile({
          //   url: 'https://api.example.com/upload',
          //   filePath: tempFilePath,
          //   name: 'avatar',
          //   success: (uploadRes) => {
          //     const data = JSON.parse(uploadRes.data);
          //     
          //     // 更新头像
          //     this.userInfo.avatar = data.url;
          //     
          //     // 保存到本地
          //     const userInfoStr = uni.getStorageSync('userInfo');
          //     if (userInfoStr) {
          //       try {
          //         const userInfo = JSON.parse(userInfoStr);
          //         userInfo.avatar = data.url;
          //         uni.setStorageSync('userInfo', JSON.stringify(userInfo));
          //       } catch (e) {
          //         console.error('解析用户信息失败', e);
          //       }
          //     }
          //     
          //     uni.showToast({
          //       title: '头像更新成功',
          //       icon: 'success'
          //     });
          //   },
          //   fail: () => {
          //     uni.showToast({
          //       title: '上传失败，请重试',
          //       icon: 'none'
          //     });
          //   },
          //   complete: () => {
          //     uni.hideLoading();
          //   }
          // });
        }
      });
    },
    
    // 前往登录页
    goToLogin() {
      uni.navigateTo({
        url: '/pages/login/login'
      });
    },
    
    // 导航到指定页面
    navigateTo(url) {
      // 检查是否需要登录
      if (url.startsWith('/pages/personal/') && !url.startsWith('/pages/personal/about') && !url.startsWith('/pages/personal/help') && !this.userInfo.id) {
        this.goToLogin();
        return;
      }
      
      uni.navigateTo({
        url: url
      });
    },
    
    // 退出登录
    logout() {
      uni.showModal({
        title: '提示',
        content: '确定要退出登录吗？',
        success: (res) => {
          if (res.confirm) {
            // 清除用户信息和token
            uni.removeStorageSync('token');
            uni.removeStorageSync('userInfo');
            
            // 更新状态
            this.userInfo = {
              id: '',
              nickname: '',
              avatar: '',
              userType: '',
              balance: '',
              equipmentCount: 0,
              couponCount: 0
            };
            
            // 提示用户
            uni.showToast({
              title: '已退出登录',
              icon: 'success'
            });
          }
        }
      });
    }
  }
}
</script>

<style>
.personal-container {
  background-color: #f8f8f8;
  min-height: 100vh;
  padding-bottom: 30rpx;
}

/* 用户卡片 */
.user-card {
  background-color: #007AFF;
  padding: 40rpx 30rpx;
  color: #fff;
  position: relative;
  margin-bottom: 20rpx;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 30rpx;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 60rpx;
  border: 4rpx solid rgba(255, 255, 255, 0.3);
  margin-right: 30rpx;
}

.user-details {
  flex: 1;
}

.nickname {
  font-size: 36rpx;
  font-weight: 500;
  margin-bottom: 10rpx;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.user-type {
  font-size: 24rpx;
  opacity: 0.9;
  background-color: rgba(255, 255, 255, 0.2);
  padding: 6rpx 16rpx;
  border-radius: 30rpx;
  display: inline-block;
}

.login-btn {
  font-size: 28rpx;
  margin-top: 10rpx;
  color: #fff;
  text-decoration: underline;
}

.user-stats {
  display: flex;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12rpx;
  padding: 20rpx 0;
}

.stat-item {
  flex: 1;
  text-align: center;
  position: relative;
}

.stat-item:not(:last-child)::after {
  content: '';
  position: absolute;
  right: 0;
  top: 20%;
  height: 60%;
  width: 1px;
  background-color: rgba(255, 255, 255, 0.2);
}

.stat-num {
  font-size: 32rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 6rpx;
}

.stat-label {
  font-size: 24rpx;
  opacity: 0.9;
}

/* 卡片样式 */
.section-card {
  background-color: #fff;
  border-radius: 12rpx;
  margin: 0 20rpx 20rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 500;
  position: relative;
  padding-left: 20rpx;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8rpx;
  width: 6rpx;
  height: 30rpx;
  background-color: #007AFF;
  border-radius: 3rpx;
}

.view-all {
  font-size: 26rpx;
  color: #999;
  display: flex;
  align-items: center;
}

.arrow {
  margin-left: 6rpx;
}

/* 订单图标 */
.order-icons {
  display: flex;
  justify-content: space-between;
}

.order-icon-item {
  text-align: center;
  position: relative;
}

.order-icon {
  width: 56rpx;
  height: 56rpx;
  margin-bottom: 10rpx;
}

.order-icon-item text {
  font-size: 24rpx;
  color: #666;
  display: block;
}

.badge {
  position: absolute;
  top: -6rpx;
  right: -6rpx;
  background-color: #ff4500;
  color: #fff;
  font-size: 20rpx;
  min-width: 32rpx;
  height: 32rpx;
  line-height: 32rpx;
  text-align: center;
  border-radius: 16rpx;
  padding: 0 6rpx;
  box-sizing: border-box;
}

/* 服务网格 */
.service-grid {
  display: flex;
  flex-wrap: wrap;
}

.service-item {
  width: 25%;
  text-align: center;
  margin-bottom: 20rpx;
}

.service-icon {
  width: 56rpx;
  height: 56rpx;
  margin-bottom: 10rpx;
}

.service-item text {
  font-size: 24rpx;
  color: #666;
  display: block;
}

/* 功能列表 */
.function-list {
  background-color: #fff;
  border-radius: 12rpx;
  margin: 0 20rpx;
  padding: 0 30rpx;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.05);
}

.function-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx 0;
  border-bottom: 1px solid #f5f5f5;
}

.function-item:last-child {
  border-bottom: none;
}

.function-name {
  font-size: 28rpx;
  color: #333;
}

.logout {
  color: #ff4500;
}
</style> 