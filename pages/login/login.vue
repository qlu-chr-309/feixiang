<template>
	<view class="login-container">
		<view class="logo-area">
			<image class="logo" src="/static/logo.png"></image>
			<text class="title">飞享 - 无人机服务平台</text>
		</view>
		
		<view class="form-area">
			<view class="input-group">
				<text class="label">用户名</text>
				<input class="input" v-model="username" placeholder="请输入用户名" />
			</view>
			
			<view class="input-group">
				<text class="label">密码</text>
				<input class="input" v-model="password" type="password" placeholder="请输入密码" />
			</view>
			
			<button class="login-btn" @click="login">登录</button>
			
			<view class="options">
				<text class="register" @click="goToRegister">注册账号</text>
				<text class="forgot-pwd">忘记密码</text>
			</view>
		</view>
		
		<view class="role-selection">
			<text class="role-title">选择角色</text>
			<view class="role-options">
				<view class="role-item" :class="{ active: role === 'personal' }" @click="selectRole('personal')">
					<text>个人买家</text>
				</view>
				<view class="role-item" :class="{ active: role === 'enterprise' }" @click="selectRole('enterprise')">
					<text>企业买家</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				username: '',
				password: '',
				role: 'personal'
			}
		},
		methods: {
			login() {
				if (!this.username || !this.password) {
					uni.showToast({
						title: '请输入用户名和密码',
						icon: 'none'
					});
					return;
				}
				
				// 实际开发中应该调用后端API进行登录验证
				// 这里模拟登录成功
				uni.showLoading({
					title: '登录中...'
				});
				
				setTimeout(() => {
					uni.hideLoading();
					uni.switchTab({
						url: '/pages/home/home'
					});
				}, 1500);
			},
			goToRegister() {
				uni.navigateTo({
					url: '/pages/login/register'
				});
			},
			selectRole(role) {
				this.role = role;
			}
		}
	}
</script>

<style>
	.login-container {
		display: flex;
		flex-direction: column;
		padding: 40rpx;
		min-height: 100vh;
		background-color: #f8f8f8;
	}
	
	.logo-area {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin: 60rpx 0;
	}
	
	.logo {
		width: 180rpx;
		height: 180rpx;
		margin-bottom: 20rpx;
	}
	
	.title {
		font-size: 36rpx;
		font-weight: bold;
		color: #333;
	}
	
	.form-area {
		background-color: #fff;
		border-radius: 16rpx;
		padding: 40rpx;
		margin-bottom: 40rpx;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
	}
	
	.input-group {
		margin-bottom: 30rpx;
	}
	
	.label {
		font-size: 28rpx;
		color: #666;
		margin-bottom: 10rpx;
		display: block;
	}
	
	.input {
		border: 2rpx solid #e5e5e5;
		height: 80rpx;
		border-radius: 8rpx;
		padding: 0 20rpx;
		font-size: 28rpx;
	}
	
	.login-btn {
		background-color: #007AFF;
		color: #fff;
		height: 90rpx;
		line-height: 90rpx;
		border-radius: 45rpx;
		font-size: 32rpx;
		margin: 40rpx 0 20rpx;
	}
	
	.options {
		display: flex;
		justify-content: space-between;
		font-size: 28rpx;
		color: #007AFF;
	}
	
	.role-selection {
		background-color: #fff;
		border-radius: 16rpx;
		padding: 40rpx;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
	}
	
	.role-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 30rpx;
		display: block;
	}
	
	.role-options {
		display: flex;
		justify-content: space-between;
	}
	
	.role-item {
		width: 48%;
		height: 100rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		border: 2rpx solid #e5e5e5;
		border-radius: 8rpx;
	}
	
	.role-item.active {
		border-color: #007AFF;
		color: #007AFF;
		background-color: rgba(0, 122, 255, 0.05);
	}
</style> 