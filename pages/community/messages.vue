<template>
	<view class="messages-container">
		<view class="header">
			<view class="back-btn" @click="goBack">
				<text class="iconfont icon-back"></text>
			</view>
			<view class="header-title">通知与消息</view>
		</view>
		
		<view class="tabs">
			<view 
				class="tab-item" 
				:class="{ active: activeTab === 'notifications' }" 
				@click="switchTab('notifications')"
			>
				通知
				<view class="badge" v-if="unreadNotifications > 0">{{unreadNotifications}}</view>
			</view>
			<view 
				class="tab-item" 
				:class="{ active: activeTab === 'messages' }" 
				@click="switchTab('messages')"
			>
				私信
				<view class="badge" v-if="unreadMessages > 0">{{unreadMessages}}</view>
			</view>
		</view>
		
		<view class="content-list" v-if="activeTab === 'notifications'">
			<view class="list-header">
				<text>全部通知</text>
				<text class="mark-read" @click="markAllRead">标记全部已读</text>
			</view>
			
			<view class="notification-item" v-for="(item, index) in notifications" :key="index" @click="viewNotification(item)">
				<view class="notification-icon" :class="item.type">
					<text class="iconfont" :class="'icon-' + item.type"></text>
				</view>
				<view class="notification-content">
					<view class="notification-title">
						<text class="username">{{item.sender}}</text>
						<text> {{item.action}}</text>
					</view>
					<text class="notification-detail">{{item.content}}</text>
					<text class="notification-time">{{item.time}}</text>
				</view>
				<view class="unread-dot" v-if="!item.read"></view>
			</view>
			
			<view class="empty-state" v-if="notifications.length === 0">
				<image src="/static/community/empty-notifications.png" class="empty-image"></image>
				<text class="empty-text">暂无通知</text>
			</view>
		</view>
		
		<view class="content-list" v-if="activeTab === 'messages'">
			<view class="message-item" v-for="(item, index) in chats" :key="index" @click="openChat(item)">
				<image :src="item.avatar" class="avatar"></image>
				<view class="message-content">
					<view class="message-header">
						<text class="username">{{item.username}}</text>
						<text class="time">{{item.lastTime}}</text>
					</view>
					<view class="message-preview">
						<text class="preview-text">{{item.lastMessage}}</text>
						<view class="message-count" v-if="item.unreadCount > 0">{{item.unreadCount}}</view>
					</view>
				</view>
			</view>
			
			<view class="empty-state" v-if="chats.length === 0">
				<image src="/static/community/empty-messages.png" class="empty-image"></image>
				<text class="empty-text">暂无私信</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				activeTab: 'notifications',
				unreadNotifications: 2,
				unreadMessages: 1,
				notifications: [
					{
						id: 1,
						type: 'like',
						sender: '航拍达人',
						action: '赞了你的帖子',
						content: '今天测试了新入手的大疆Mini 3 Pro，续航和画质都超出预期...',
						time: '10分钟前',
						read: false
					},
					{
						id: 2,
						type: 'comment',
						sender: '无人机教练',
						action: '回复了你的评论',
						content: '对于初学者来说，建议从小型无人机开始练习，掌握基本操作后再升级...',
						time: '30分钟前',
						read: false
					},
					{
						id: 3,
						type: 'system',
						sender: '系统消息',
						action: '您的提问已被回答',
						content: '您关于"大疆Mini 3 Pro是否适合新手入门"的提问已有新回答',
						time: '2小时前',
						read: true
					},
					{
						id: 4,
						type: 'follow',
						sender: '飞行专家',
						action: '关注了你',
						content: '',
						time: '昨天',
						read: true
					}
				],
				chats: [
					{
						id: 1,
						username: '航拍达人',
						avatar: '/static/community/avatar1.jpg',
						lastMessage: '你好，我想请教一下你使用的是什么型号的无人机？',
						lastTime: '昨天',
						unreadCount: 1
					},
					{
						id: 2,
						username: '植保技术员',
						avatar: '/static/community/avatar2.jpg',
						lastMessage: '谢谢分享，这些技巧对我很有帮助！',
						lastTime: '2023-04-08',
						unreadCount: 0
					},
					{
						id: 3,
						username: '无人机维修师',
						avatar: '/static/community/avatar3.jpg',
						lastMessage: '你好，根据你描述的问题，可能是电机出现了故障，建议检查一下电机连接...',
						lastTime: '2023-04-05',
						unreadCount: 0
					}
				]
			}
		},
		computed: {
			unreadNotificationCount() {
				return this.notifications.filter(item => !item.read).length;
			}
		},
		methods: {
			goBack() {
				uni.navigateBack();
			},
			switchTab(tab) {
				this.activeTab = tab;
			},
			markAllRead() {
				this.notifications.forEach(item => {
					item.read = true;
				});
				this.unreadNotifications = 0;
			},
			viewNotification(notification) {
				notification.read = true;
				this.unreadNotifications = this.unreadNotificationCount;
				// 根据通知类型跳转到相应页面
				uni.showToast({
					title: '查看通知: ' + notification.id,
					icon: 'none'
				});
			},
			openChat(chat) {
				uni.navigateTo({
					url: '/pages/community/chat?id=' + chat.id + '&username=' + chat.username
				});
			}
		}
	}
</script>

<style>
	.messages-container {
		min-height: 100vh;
		background-color: #f5f5f5;
	}
	
	.header {
		background-color: #007AFF;
		padding: 20rpx 30rpx;
		color: #fff;
		display: flex;
		align-items: center;
		position: relative;
	}
	
	.back-btn {
		position: absolute;
		left: 30rpx;
	}
	
	.header-title {
		flex: 1;
		font-size: 36rpx;
		font-weight: bold;
		text-align: center;
	}
	
	.tabs {
		display: flex;
		background-color: #fff;
		border-bottom: 1rpx solid #eee;
		position: sticky;
		top: 0;
		z-index: 10;
	}
	
	.tab-item {
		flex: 1;
		text-align: center;
		padding: 24rpx 0;
		font-size: 28rpx;
		color: #666;
		position: relative;
	}
	
	.tab-item.active {
		color: #007AFF;
		font-weight: bold;
	}
	
	.tab-item.active::after {
		content: '';
		position: absolute;
		bottom: 0;
		left: 50%;
		transform: translateX(-50%);
		width: 60rpx;
		height: 6rpx;
		background-color: #007AFF;
		border-radius: 3rpx;
	}
	
	.badge {
		position: absolute;
		top: 10rpx;
		right: 50%;
		margin-right: -60rpx;
		background-color: #ff4d4f;
		color: #fff;
		font-size: 20rpx;
		min-width: 32rpx;
		height: 32rpx;
		border-radius: 16rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0 6rpx;
	}
	
	.content-list {
		padding: 0;
	}
	
	.list-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 20rpx 30rpx;
		font-size: 26rpx;
		color: #666;
		background-color: #fff;
		border-bottom: 1rpx solid #f0f0f0;
	}
	
	.mark-read {
		color: #007AFF;
	}
	
	.notification-item {
		display: flex;
		padding: 24rpx 30rpx;
		background-color: #fff;
		border-bottom: 1rpx solid #f0f0f0;
		position: relative;
	}
	
	.notification-icon {
		width: 80rpx;
		height: 80rpx;
		border-radius: 40rpx;
		background-color: #e6f7ff;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 20rpx;
	}
	
	.notification-icon.like {
		background-color: #fff2f0;
	}
	
	.notification-icon.comment {
		background-color: #e6fffb;
	}
	
	.notification-icon.system {
		background-color: #f9f0ff;
	}
	
	.notification-icon.follow {
		background-color: #f6ffed;
	}
	
	.notification-icon .iconfont {
		font-size: 40rpx;
		color: #1890ff;
	}
	
	.notification-icon .icon-like {
		color: #ff4d4f;
	}
	
	.notification-icon .icon-comment {
		color: #13c2c2;
	}
	
	.notification-icon .icon-system {
		color: #722ed1;
	}
	
	.notification-icon .icon-follow {
		color: #52c41a;
	}
	
	.notification-content {
		flex: 1;
	}
	
	.notification-title {
		font-size: 28rpx;
		color: #333;
		margin-bottom: 8rpx;
	}
	
	.username {
		font-weight: bold;
	}
	
	.notification-detail {
		font-size: 26rpx;
		color: #666;
		display: block;
		margin-bottom: 8rpx;
		line-height: 1.5;
	}
	
	.notification-time {
		font-size: 24rpx;
		color: #999;
		display: block;
	}
	
	.unread-dot {
		width: 16rpx;
		height: 16rpx;
		border-radius: 8rpx;
		background-color: #ff4d4f;
		position: absolute;
		right: 30rpx;
		top: 24rpx;
	}
	
	.message-item {
		display: flex;
		padding: 24rpx 30rpx;
		background-color: #fff;
		border-bottom: 1rpx solid #f0f0f0;
	}
	
	.avatar {
		width: 100rpx;
		height: 100rpx;
		border-radius: 50rpx;
		margin-right: 20rpx;
	}
	
	.message-content {
		flex: 1;
	}
	
	.message-header {
		display: flex;
		justify-content: space-between;
		margin-bottom: 10rpx;
	}
	
	.username {
		font-size: 30rpx;
		font-weight: bold;
		color: #333;
	}
	
	.time {
		font-size: 24rpx;
		color: #999;
	}
	
	.message-preview {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.preview-text {
		font-size: 26rpx;
		color: #666;
		flex: 1;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	
	.message-count {
		background-color: #ff4d4f;
		color: #fff;
		font-size: 20rpx;
		min-width: 32rpx;
		height: 32rpx;
		border-radius: 16rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0 6rpx;
		margin-left: 10rpx;
	}
	
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
		margin-bottom: 30rpx;
	}
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
	}
</style> 