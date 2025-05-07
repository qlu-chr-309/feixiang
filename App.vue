<script>
	export default {
		globalData: {
			userInfo: null,
			isLoggedIn: false,
			userRole: '' // 'buyer' or 'supplier'
		},
		onLaunch: function() {
			console.log('App Launch');
			// 检查登录状态
			this.checkLoginStatus();
		},
		onShow: function() {
			console.log('App Show');
		},
		onHide: function() {
			console.log('App Hide');
		},
		methods: {
			checkLoginStatus() {
				// 实际开发中从缓存或云端获取用户登录状态
				const token = uni.getStorageSync('token');
				if (token) {
					// 此处应校验token有效性，可能需要调用后端API
					// 设置为已登录，实际开发中应根据后端返回设置
					this.globalData.isLoggedIn = true;
					this.globalData.userRole = uni.getStorageSync('userRole') || 'buyer';
					// 获取用户信息
					this.getUserInfo();
				} else {
					this.globalData.isLoggedIn = false;
					this.globalData.userInfo = null;
				}
			},
			getUserInfo() {
				// 实际开发中应调用API获取最新用户信息
				const cachedUserInfo = uni.getStorageSync('userInfo');
				if (cachedUserInfo) {
					this.globalData.userInfo = JSON.parse(cachedUserInfo);
				}
			}
		}
	}
</script>

<style>
	/* 全局CSS */
	page {
		font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei', sans-serif;
		font-size: 28rpx;
		line-height: 1.5;
		color: #333;
		background-color: #f5f5f5;
		-webkit-font-smoothing: antialiased;
		box-sizing: border-box;
	}
	
	view, text, navigator, input, textarea, button, image {
		box-sizing: border-box;
	}
	
	/* 清除浮动 */
	.clearfix:after {
		content: '';
		display: block;
		clear: both;
	}
	
	/* 单行文本省略 */
	.ellipsis {
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
	}
	
	/* 多行文本省略 */
	.multi-ellipsis-2 {
		overflow: hidden;
		text-overflow: ellipsis;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
	}
	
	/* 常用颜色 */
	.text-primary {
		color: #007AFF;
	}
	
	.text-success {
		color: #4cd964;
	}
	
	.text-warning {
		color: #f0ad4e;
	}
	
	.text-danger {
		color: #dd524d;
	}
	
	.text-info {
		color: #909399;
	}
	
	/* 常用间距 */
	.m-10 {
		margin: 10rpx;
	}
	
	.m-20 {
		margin: 20rpx;
	}
	
	.m-30 {
		margin: 30rpx;
	}
	
	.mt-10 {
		margin-top: 10rpx;
	}
	
	.mt-20 {
		margin-top: 20rpx;
	}
	
	.mt-30 {
		margin-top: 30rpx;
	}
	
	.mb-10 {
		margin-bottom: 10rpx;
	}
	
	.mb-20 {
		margin-bottom: 20rpx;
	}
	
	.mb-30 {
		margin-bottom: 30rpx;
	}
	
	.ml-10 {
		margin-left: 10rpx;
	}
	
	.ml-20 {
		margin-left: 20rpx;
	}
	
	.mr-10 {
		margin-right: 10rpx;
	}
	
	.mr-20 {
		margin-right: 20rpx;
	}
	
	.p-10 {
		padding: 10rpx;
	}
	
	.p-20 {
		padding: 20rpx;
	}
	
	.p-30 {
		padding: 30rpx;
	}
	
	/* 按钮样式 */
	.btn {
		padding: 20rpx 30rpx;
		border-radius: 10rpx;
		text-align: center;
		font-size: 28rpx;
	}
	
	.btn-primary {
		background-color: #007AFF;
		color: #fff;
	}
	
	.btn-outline {
		background-color: transparent;
		color: #007AFF;
		border: 1rpx solid #007AFF;
	}
	
	.btn-block {
		display: block;
		width: 100%;
	}
	
	/* 阴影效果 */
	.shadow {
		box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.1);
	}
	
	/* 卡片样式 */
	.card {
		background-color: #fff;
		border-radius: 12rpx;
		padding: 20rpx;
		margin-bottom: 20rpx;
	}
</style>
