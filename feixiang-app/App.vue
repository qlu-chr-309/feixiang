<script>
export default {
  onLaunch: function() {
    console.log('App Launch')
    // 检查是否有登录Token
    const token = uni.getStorageSync('token')
    if (token) {
      // 有token尝试自动登录
      this.$store.setToken(token)
      const userInfo = uni.getStorageSync('userInfo')
      if (userInfo) {
        this.$store.setUserInfo(JSON.parse(userInfo))
      }
    }
  },
  onShow: function() {
    console.log('App Show')
  },
  onHide: function() {
    console.log('App Hide')
  }
}
</script>

<style>
/* 全局样式 */
page {
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background-color: #f8f8f8;
  font-size: 14px;
  color: #333;
  box-sizing: border-box;
}

.container {
  padding: 20rpx;
}

/* 按钮样式 */
.btn-primary {
  background-color: #007AFF;
  color: #ffffff;
  border-radius: 4px;
}

.btn-secondary {
  background-color: #F0F0F0;
  color: #333333;
  border-radius: 4px;
}

/* 卡片样式 */
.card {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 20rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 列表样式 */
.list-item {
  display: flex;
  padding: 20rpx 0;
  border-bottom: 1px solid #eeeeee;
}

/* 表单样式 */
.form-group {
  margin-bottom: 20rpx;
}

.form-label {
  display: block;
  margin-bottom: 10rpx;
  font-weight: bold;
}

.form-input {
  width: 100%;
  height: 80rpx;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0 20rpx;
  box-sizing: border-box;
}

.form-textarea {
  width: 100%;
  height: 200rpx;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10rpx 20rpx;
  box-sizing: border-box;
}
</style> 