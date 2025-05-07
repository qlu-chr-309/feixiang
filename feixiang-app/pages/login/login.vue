<template>
  <view class="login-container">
    <view class="login-header">
      <image class="logo" src="/static/images/logo.png" mode="aspectFit"></image>
      <text class="title">飞享平台</text>
      <text class="subtitle">无人机行业一站式服务</text>
    </view>
    
    <view class="login-form">
      <view class="form-group">
        <text class="form-label">手机号码</text>
        <input class="form-input" type="number" maxlength="11" placeholder="请输入手机号码" v-model="phone" />
      </view>
      
      <view class="form-group">
        <text class="form-label">验证码</text>
        <view class="code-input-container">
          <input class="form-input code-input" type="number" maxlength="6" placeholder="请输入验证码" v-model="code" />
          <button class="code-btn" :disabled="isSending" @click="sendCode">{{sendBtnText}}</button>
        </view>
      </view>
      
      <button class="login-btn" @click="login">登录</button>
      
      <view class="agreement">
        <checkbox :checked="agreedPolicy" @tap="toggleAgreement"></checkbox>
        <text class="agreement-text">同意<text class="link">用户协议</text>和<text class="link">隐私政策</text></text>
      </view>
    </view>
    
    <view class="role-select-btn" @click="goToRoleSelect">选择身份</view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      phone: '',
      code: '',
      agreedPolicy: false,
      isSending: false,
      countdown: 60,
      sendBtnText: '获取验证码',
      timer: null
    }
  },
  methods: {
    sendCode() {
      // 手机号验证
      if (!/^1\d{10}$/.test(this.phone)) {
        uni.showToast({
          title: '请输入正确的手机号码',
          icon: 'none'
        });
        return;
      }
      
      this.isSending = true;
      this.countdown = 60;
      this.sendBtnText = `${this.countdown}s`;
      
      // 发送验证码请求
      this.$request({
        url: '/auth/sendCode',
        method: 'POST',
        data: {
          phone: this.phone
        }
      }).then(res => {
        uni.showToast({
          title: '验证码已发送',
          icon: 'none'
        });
        
        // 开始倒计时
        this.timer = setInterval(() => {
          this.countdown--;
          this.sendBtnText = `${this.countdown}s`;
          
          if (this.countdown <= 0) {
            clearInterval(this.timer);
            this.isSending = false;
            this.sendBtnText = '获取验证码';
          }
        }, 1000);
      }).catch(err => {
        this.isSending = false;
        this.sendBtnText = '获取验证码';
      });
    },
    
    login() {
      // 验证表单
      if (!/^1\d{10}$/.test(this.phone)) {
        uni.showToast({
          title: '请输入正确的手机号码',
          icon: 'none'
        });
        return;
      }
      
      if (!this.code || this.code.length !== 6) {
        uni.showToast({
          title: '请输入6位验证码',
          icon: 'none'
        });
        return;
      }
      
      if (!this.agreedPolicy) {
        uni.showToast({
          title: '请同意用户协议和隐私政策',
          icon: 'none'
        });
        return;
      }
      
      // 登录请求
      this.$request({
        url: '/auth/login',
        method: 'POST',
        data: {
          phone: this.phone,
          code: this.code
        }
      }).then(res => {
        // 保存用户信息和token
        this.$store.setToken(res.token);
        this.$store.setUserInfo(res.userInfo);
        
        // 保存到本地存储
        uni.setStorageSync('userInfo', JSON.stringify(res.userInfo));
        
        uni.showToast({
          title: '登录成功',
          icon: 'success'
        });
        
        // 根据用户状态跳转
        if (res.userInfo.hasSelectRole) {
          uni.switchTab({
            url: '/pages/home/home'
          });
        } else {
          uni.navigateTo({
            url: '/pages/roleSelect/roleSelect'
          });
        }
      }).catch(err => {
        console.error('登录失败', err);
      });
    },
    
    toggleAgreement() {
      this.agreedPolicy = !this.agreedPolicy;
    },
    
    goToRoleSelect() {
      uni.navigateTo({
        url: '/pages/roleSelect/roleSelect'
      });
    }
  },
  onUnload() {
    // 清除定时器
    if (this.timer) {
      clearInterval(this.timer);
    }
  }
}
</script>

<style>
.login-container {
  padding: 40rpx;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.login-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 80rpx;
  margin-top: 60rpx;
}

.logo {
  width: 160rpx;
  height: 160rpx;
  margin-bottom: 20rpx;
}

.title {
  font-size: 40rpx;
  font-weight: bold;
  margin-bottom: 10rpx;
}

.subtitle {
  font-size: 28rpx;
  color: #666;
}

.login-form {
  margin-bottom: 40rpx;
}

.form-group {
  margin-bottom: 30rpx;
}

.form-label {
  display: block;
  margin-bottom: 10rpx;
  font-size: 28rpx;
}

.form-input {
  width: 100%;
  height: 80rpx;
  background-color: #f5f5f5;
  border-radius: 8rpx;
  padding: 0 20rpx;
  box-sizing: border-box;
}

.code-input-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.code-input {
  flex: 1;
  margin-right: 20rpx;
}

.code-btn {
  width: 200rpx;
  height: 80rpx;
  line-height: 80rpx;
  font-size: 26rpx;
  background-color: #007AFF;
  color: #fff;
}

.code-btn[disabled] {
  background-color: #ccc;
  color: #fff;
}

.login-btn {
  width: 100%;
  height: 90rpx;
  line-height: 90rpx;
  background-color: #007AFF;
  color: #fff;
  border-radius: 8rpx;
  font-size: 32rpx;
  margin-top: 60rpx;
  margin-bottom: 30rpx;
}

.agreement {
  display: flex;
  align-items: center;
  font-size: 24rpx;
  color: #666;
}

.agreement-text {
  margin-left: 10rpx;
}

.link {
  color: #007AFF;
}

.role-select-btn {
  text-align: center;
  margin-top: auto;
  color: #007AFF;
  font-size: 28rpx;
  padding: 20rpx 0;
}
</style> 