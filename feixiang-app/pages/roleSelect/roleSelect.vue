<template>
  <view class="role-select-container">
    <view class="header">
      <text class="title">选择您的身份</text>
      <text class="subtitle">根据您的需求选择合适的身份</text>
    </view>
    
    <view class="role-cards">
      <view class="role-card" :class="{ active: selectedRole === 'personal' }" @click="selectRole('personal')">
        <image class="role-icon" src="/static/images/personal-icon.png" mode="aspectFit"></image>
        <text class="role-name">个人买家(爱好者)</text>
        <text class="role-desc">适合个人无人机爱好者使用</text>
        <view class="role-features">
          <view class="feature-item">
            <text class="feature-icon">✓</text>
            <text class="feature-text">发布设备需求</text>
          </view>
          <view class="feature-item">
            <text class="feature-icon">✓</text>
            <text class="feature-text">租赁无人机设备</text>
          </view>
          <view class="feature-item">
            <text class="feature-icon">✓</text>
            <text class="feature-text">参与社区交流</text>
          </view>
        </view>
      </view>
      
      <view class="role-card" :class="{ active: selectedRole === 'enterprise' }" @click="selectRole('enterprise')">
        <image class="role-icon" src="/static/images/enterprise-icon.png" mode="aspectFit"></image>
        <text class="role-name">企业买家(采购方)</text>
        <text class="role-desc">适合企业级采购和项目需求</text>
        <view class="role-features">
          <view class="feature-item">
            <text class="feature-icon">✓</text>
            <text class="feature-text">发布批量采购需求</text>
          </view>
          <view class="feature-item">
            <text class="feature-icon">✓</text>
            <text class="feature-text">对接专业服务商</text>
          </view>
          <view class="feature-item">
            <text class="feature-icon">✓</text>
            <text class="feature-text">项目全流程管理</text>
          </view>
          <view class="feature-item">
            <text class="feature-icon">✓</text>
            <text class="feature-text">多订单成本预算</text>
          </view>
        </view>
      </view>
    </view>
    
    <button class="confirm-btn" :disabled="!selectedRole" @click="confirmSelect">确认选择</button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      selectedRole: ''
    }
  },
  methods: {
    selectRole(role) {
      this.selectedRole = role;
    },
    confirmSelect() {
      if (!this.selectedRole) {
        uni.showToast({
          title: '请选择身份',
          icon: 'none'
        });
        return;
      }
      
      // 设置用户类型
      this.$store.setUserType(this.selectedRole);
      
      // 更新用户信息
      this.$request({
        url: '/user/updateRole',
        method: 'POST',
        data: {
          role: this.selectedRole
        }
      }).then(res => {
        uni.showToast({
          title: '设置成功',
          icon: 'success'
        });
        
        // 跳转到首页
        setTimeout(() => {
          uni.switchTab({
            url: '/pages/home/home'
          });
        }, 1000);
      }).catch(err => {
        console.error('设置身份失败', err);
      });
    }
  }
}
</script>

<style>
.role-select-container {
  padding: 40rpx;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 60rpx;
  margin-top: 40rpx;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 10rpx;
  display: block;
}

.subtitle {
  font-size: 28rpx;
  color: #666;
}

.role-cards {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
  margin-bottom: 60rpx;
}

.role-card {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
  position: relative;
  border: 2rpx solid transparent;
  transition: all 0.3s;
}

.role-card.active {
  border-color: #007AFF;
  background-color: rgba(0, 122, 255, 0.05);
}

.role-icon {
  width: 80rpx;
  height: 80rpx;
  margin-bottom: 20rpx;
}

.role-name {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 10rpx;
  display: block;
}

.role-desc {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 30rpx;
  display: block;
}

.role-features {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.feature-item {
  display: flex;
  align-items: center;
}

.feature-icon {
  color: #007AFF;
  margin-right: 10rpx;
  font-weight: bold;
}

.feature-text {
  font-size: 26rpx;
  color: #333;
}

.confirm-btn {
  width: 100%;
  height: 90rpx;
  line-height: 90rpx;
  background-color: #007AFF;
  color: #fff;
  border-radius: 8rpx;
  font-size: 32rpx;
  margin-top: auto;
}

.confirm-btn[disabled] {
  background-color: #cccccc;
  color: #ffffff;
}
</style> 