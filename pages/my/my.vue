<template>
	<view class="my-container">
		<!-- 用户信息区域 -->
		<view class="user-info-section">
			<view class="user-basic">
				<image class="avatar" :src="userInfo.avatar || '/static/default-avatar.png'"></image>
				<view class="user-detail">
					<text class="username">{{userInfo.nickname || '未登录'}}</text>
					<view class="user-role" v-if="userInfo.isLoggedIn">
						<text class="role-text">{{userInfo.role === 'buyer' ? '采购方' : '供应商'}}</text>
					</view>
					<view class="login-btn" v-else @click="toLogin">
						<text>立即登录</text>
					</view>
				</view>
			</view>
			<view class="user-stats">
				<view class="stat-item" @click="navigateTo('/pages/my/orders')">
					<text class="stat-number">{{userInfo.orderCount || 0}}</text>
					<text class="stat-label">我的订单</text>
				</view>
				<view class="stat-item" @click="navigateTo('/pages/my/favorites')">
					<text class="stat-number">{{userInfo.favoriteCount || 0}}</text>
					<text class="stat-label">我的收藏</text>
				</view>
				<view class="stat-item" @click="navigateTo('/pages/my/coupons')">
					<text class="stat-number">{{userInfo.couponCount || 0}}</text>
					<text class="stat-label">优惠券</text>
				</view>
			</view>
		</view>
		
		<!-- 订单区域 -->
		<view class="order-section" v-if="userInfo.isLoggedIn">
			<view class="section-header">
				<text class="section-title">我的订单</text>
				<view class="view-all" @click="navigateTo('/pages/my/orders')">
					<text>查看全部</text>
					<text class="iconfont icon-right"></text>
				</view>
			</view>
			<view class="order-status">
				<view class="status-item" @click="navigateTo('/pages/my/orders?status=unpaid')">
					<view class="status-icon">
						<text class="iconfont icon-wallet"></text>
						<text class="badge" v-if="orderCounts.unpaid > 0">{{orderCounts.unpaid}}</text>
					</view>
					<text class="status-text">待付款</text>
				</view>
				<view class="status-item" @click="navigateTo('/pages/my/orders?status=processing')">
					<view class="status-icon">
						<text class="iconfont icon-plane"></text>
						<text class="badge" v-if="orderCounts.processing > 0">{{orderCounts.processing}}</text>
					</view>
					<text class="status-text">进行中</text>
				</view>
				<view class="status-item" @click="navigateTo('/pages/my/orders?status=completed')">
					<view class="status-icon">
						<text class="iconfont icon-check"></text>
						<text class="badge" v-if="orderCounts.completed > 0">{{orderCounts.completed}}</text>
					</view>
					<text class="status-text">已完成</text>
				</view>
				<view class="status-item" @click="navigateTo('/pages/my/orders?status=review')">
					<view class="status-icon">
						<text class="iconfont icon-comment"></text>
						<text class="badge" v-if="orderCounts.review > 0">{{orderCounts.review}}</text>
					</view>
					<text class="status-text">待评价</text>
				</view>
				<view class="status-item" @click="navigateTo('/pages/my/orders?status=aftersale')">
					<view class="status-icon">
						<text class="iconfont icon-service"></text>
						<text class="badge" v-if="orderCounts.aftersale > 0">{{orderCounts.aftersale}}</text>
					</view>
					<text class="status-text">售后</text>
				</view>
			</view>
		</view>
		
		<!-- 功能菜单 -->
		<view class="menu-section">
			<view class="menu-group">
				<view class="menu-item" @click="navigateTo('/pages/my/profile')">
					<text class="iconfont icon-user menu-icon"></text>
					<text class="menu-text">个人资料</text>
					<text class="iconfont icon-right"></text>
				</view>
				<view class="menu-item" @click="navigateTo('/pages/my/supplier')" v-if="userInfo.role === 'buyer'">
					<text class="iconfont icon-supplier menu-icon"></text>
					<text class="menu-text">供应商管理</text>
					<text class="iconfont icon-right"></text>
				</view>
				<view class="menu-item" @click="navigateTo('/pages/my/services')" v-if="userInfo.role === 'supplier'">
					<text class="iconfont icon-service menu-icon"></text>
					<text class="menu-text">我的服务</text>
					<text class="iconfont icon-right"></text>
				</view>
				<view class="menu-item" @click="navigateTo('/pages/my/wallet')">
					<text class="iconfont icon-wallet menu-icon"></text>
					<text class="menu-text">我的钱包</text>
					<text class="iconfont icon-right"></text>
				</view>
			</view>
			
			<view class="menu-group">
				<view class="menu-item" @click="navigateTo('/pages/my/address')">
					<text class="iconfont icon-location menu-icon"></text>
					<text class="menu-text">收货地址</text>
					<text class="iconfont icon-right"></text>
				</view>
				<view class="menu-item" @click="navigateTo('/pages/my/message')">
					<text class="iconfont icon-message menu-icon"></text>
					<text class="menu-text">消息中心</text>
					<text class="badge" v-if="messageCounts > 0">{{messageCounts}}</text>
					<text class="iconfont icon-right"></text>
				</view>
			</view>
			
			<view class="menu-group">
				<view class="menu-item" @click="navigateTo('/pages/my/feedback')">
					<text class="iconfont icon-feedback menu-icon"></text>
					<text class="menu-text">意见反馈</text>
					<text class="iconfont icon-right"></text>
				</view>
				<view class="menu-item" @click="navigateTo('/pages/my/help')">
					<text class="iconfont icon-help menu-icon"></text>
					<text class="menu-text">帮助中心</text>
					<text class="iconfont icon-right"></text>
				</view>
				<view class="menu-item" @click="navigateTo('/pages/my/settings')">
					<text class="iconfont icon-settings menu-icon"></text>
					<text class="menu-text">设置</text>
					<text class="iconfont icon-right"></text>
				</view>
			</view>
		</view>
		
		<!-- 退出登录按钮 -->
		<view class="logout-btn" v-if="userInfo.isLoggedIn" @click="logout">
			<text>退出登录</text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				userInfo: {
					isLoggedIn: true, // 实际开发中应从全局状态或缓存中获取
					nickname: '张先生',
					avatar: '/static/avatar.png',
					role: 'buyer',
					orderCount: 12,
					favoriteCount: 8,
					couponCount: 3
				},
				orderCounts: {
					unpaid: 2,
					processing: 3,
					completed: 5,
					review: 1,
					aftersale: 0
				},
				messageCounts: 5
			}
		},
		methods: {
			navigateTo(url) {
				uni.navigateTo({
					url: url
				});
			},
			toLogin() {
				uni.navigateTo({
					url: '/pages/login/login'
				});
			},
			logout() {
				// 实际开发中应调用登出API并清除本地登录状态
				uni.showModal({
					title: '提示',
					content: '确定要退出登录吗？',
					success: (res) => {
						if (res.confirm) {
							this.userInfo.isLoggedIn = false;
							this.userInfo.nickname = '';
							this.userInfo.avatar = '';
							// 可能还需要重置其他状态或跳转到登录页
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
	.my-container {
		min-height: 100vh;
		background-color: #f5f5f5;
		padding-bottom: 40rpx;
	}
	
	.user-info-section {
		background-color: #007AFF;
		color: #fff;
		padding: 40rpx 30rpx;
	}
	
	.user-basic {
		display: flex;
		align-items: center;
		margin-bottom: 30rpx;
	}
	
	.avatar {
		width: 120rpx;
		height: 120rpx;
		border-radius: 60rpx;
		margin-right: 30rpx;
		border: 4rpx solid rgba(255, 255, 255, 0.3);
	}
	
	.user-detail {
		flex: 1;
	}
	
	.username {
		font-size: 36rpx;
		font-weight: bold;
		margin-bottom: 10rpx;
		display: block;
	}
	
	.user-role {
		display: inline-block;
		background-color: rgba(255, 255, 255, 0.2);
		padding: 6rpx 20rpx;
		border-radius: 30rpx;
	}
	
	.role-text {
		font-size: 24rpx;
	}
	
	.login-btn {
		display: inline-block;
		background-color: #fff;
		color: #007AFF;
		padding: 10rpx 30rpx;
		border-radius: 30rpx;
		font-size: 28rpx;
		font-weight: bold;
	}
	
	.user-stats {
		display: flex;
		justify-content: space-around;
		text-align: center;
	}
	
	.stat-number {
		font-size: 32rpx;
		font-weight: bold;
		display: block;
		margin-bottom: 4rpx;
	}
	
	.stat-label {
		font-size: 24rpx;
		opacity: 0.8;
	}
	
	.order-section {
		background-color: #fff;
		margin: 20rpx;
		border-radius: 12rpx;
		padding: 30rpx;
	}
	
	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 30rpx;
	}
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
	}
	
	.view-all {
		font-size: 26rpx;
		color: #999;
		display: flex;
		align-items: center;
	}
	
	.icon-right {
		margin-left: 4rpx;
		font-size: 24rpx;
	}
	
	.order-status {
		display: flex;
		justify-content: space-between;
	}
	
	.status-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 20%;
	}
	
	.status-icon {
		position: relative;
		margin-bottom: 10rpx;
	}
	
	.status-icon .iconfont {
		font-size: 48rpx;
		color: #007AFF;
	}
	
	.badge {
		position: absolute;
		top: -10rpx;
		right: -10rpx;
		background-color: #ff4d4f;
		color: #fff;
		font-size: 20rpx;
		min-width: 30rpx;
		height: 30rpx;
		line-height: 30rpx;
		text-align: center;
		border-radius: 15rpx;
		padding: 0 6rpx;
	}
	
	.status-text {
		font-size: 24rpx;
		color: #666;
	}
	
	.menu-section {
		padding: 0 20rpx;
	}
	
	.menu-group {
		background-color: #fff;
		border-radius: 12rpx;
		margin-bottom: 20rpx;
		overflow: hidden;
	}
	
	.menu-item {
		display: flex;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1rpx solid #f5f5f5;
	}
	
	.menu-item:last-child {
		border-bottom: none;
	}
	
	.menu-icon {
		width: 40rpx;
		font-size: 40rpx;
		margin-right: 20rpx;
		color: #007AFF;
	}
	
	.menu-text {
		flex: 1;
		font-size: 28rpx;
		color: #333;
	}
	
	.logout-btn {
		margin: 40rpx 20rpx;
		height: 90rpx;
		line-height: 90rpx;
		text-align: center;
		background-color: #fff;
		border-radius: 45rpx;
		font-size: 30rpx;
		color: #ff4d4f;
	}
</style> 