<template>
	<view class="community-container">
		<view class="header">
			<view class="header-title">社区交流</view>
		</view>
		
		<view class="menu-card">
			<view class="community-item" @click="navigateTo('/pages/community/myPosts')">
				<view class="community-icon">
					<text class="iconfont icon-posts"></text>
				</view>
				<view class="community-info">
					<text class="community-title">我发布的</text>
					<text class="community-count">{{communityData.postCount}}条发布</text>
				</view>
				<text class="iconfont icon-right"></text>
			</view>
			
			<view class="community-item" @click="navigateTo('/pages/community/messages')">
				<view class="community-icon message-icon">
					<text class="iconfont icon-message"></text>
					<text class="badge" v-if="communityData.unreadCount > 0">{{communityData.unreadCount}}</text>
				</view>
				<view class="community-info">
					<text class="community-title">通知与消息</text>
					<text class="community-count">{{communityData.unreadCount}}条未读</text>
				</view>
				<text class="iconfont icon-right"></text>
			</view>
			
			<view class="community-item" @click="navigateTo('/pages/community/events')">
				<view class="community-icon event-icon">
					<text class="iconfont icon-event"></text>
				</view>
				<view class="community-info">
					<text class="community-title">赛事信息</text>
					<text class="community-count">{{communityData.eventCount}}场比赛</text>
				</view>
				<text class="iconfont icon-right"></text>
			</view>
		</view>
		
		<view class="section-title">热门话题</view>
		<view class="topic-list">
			<view class="topic-item" v-for="(item, index) in topicList" :key="index" @click="navigateTo(item.url)">
				<image :src="item.image" mode="aspectFill" class="topic-image"></image>
				<view class="topic-info">
					<text class="topic-title">{{item.title}}</text>
					<view class="topic-meta">
						<text class="topic-tag">#{{item.tag}}</text>
						<text class="topic-count">{{item.discussCount}}人参与</text>
					</view>
				</view>
			</view>
		</view>
		
		<view class="section-title">最新动态</view>
		<view class="post-list">
			<view class="post-item" v-for="(item, index) in postList" :key="index" @click="viewPostDetail(item.id)">
				<view class="post-header">
					<image :src="item.avatar" class="post-avatar"></image>
					<view class="post-user-info">
						<text class="post-username">{{item.username}}</text>
						<text class="post-time">{{item.time}}</text>
					</view>
				</view>
				<text class="post-content">{{item.content}}</text>
				<view class="post-images" v-if="item.images && item.images.length > 0">
					<image 
						v-for="(img, imgIndex) in item.images" 
						:key="imgIndex" 
						:src="img" 
						mode="aspectFill" 
						class="post-image"
					></image>
				</view>
				<view class="post-actions">
					<view class="post-action">
						<text class="iconfont icon-like"></text>
						<text class="action-count">{{item.likeCount}}</text>
					</view>
					<view class="post-action">
						<text class="iconfont icon-comment"></text>
						<text class="action-count">{{item.commentCount}}</text>
					</view>
					<view class="post-action">
						<text class="iconfont icon-share"></text>
						<text class="action-count">{{item.shareCount}}</text>
					</view>
				</view>
			</view>
		</view>
		
		<view class="float-btn" @click="createPost">
			<text class="iconfont icon-add"></text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				communityData: {
					postCount: 5,
					unreadCount: 3,
					eventCount: 8
				},
				topicList: [
					{
						title: '2023无人机创新大赛',
						tag: '竞技赛事',
						discussCount: 128,
						image: '/static/tabbar/home.png',
						url: '/pages/community/topic?id=1'
					},
					{
						title: '无人机新手入门指南',
						tag: '经验分享',
						discussCount: 89,
						image: '/static/tabbar/service.png',
						url: '/pages/community/topic?id=2'
					},
					{
						title: '植保无人机使用技巧',
						tag: '技术交流',
						discussCount: 56,
						image: '/static/tabbar/demand.png',
						url: '/pages/community/topic?id=3'
					}
				],
				postList: [
					{
						id: 1,
						username: '云端飞手',
						avatar: '/static/tabbar/my.png',
						time: '10分钟前',
						content: '今天参加了无人机飞行比赛，终于拿到了自己的第一个奖杯！感谢一路上支持我的各位飞友！',
						images: ['/static/tabbar/home.png', '/static/tabbar/service.png'],
						likeCount: 38,
						commentCount: 12,
						shareCount: 5
					},
					{
						id: 2,
						username: '航拍达人',
						avatar: '/static/tabbar/demand.png',
						time: '2小时前',
						content: '分享一组昨天拍摄的日落航拍照片，大家觉得怎么样？',
						images: ['/static/tabbar/community.png'],
						likeCount: 56,
						commentCount: 8,
						shareCount: 15
					}
				]
			}
		},
		methods: {
			navigateTo(url) {
				uni.navigateTo({
					url: url
				});
			},
			viewPostDetail(id) {
				uni.navigateTo({
					url: '/pages/community/postDetail?id=' + id
				});
			},
			createPost() {
				uni.navigateTo({
					url: '/pages/community/createPost'
				});
			}
		}
	}
</script>

<style>
	.community-container {
		min-height: 100vh;
		padding-bottom: 120rpx;
		background-color: #f5f5f5;
		position: relative;
	}
	
	.header {
		background-color: #007AFF;
		padding: 20rpx 30rpx;
		color: #fff;
	}
	
	.header-title {
		font-size: 36rpx;
		font-weight: bold;
		text-align: center;
	}
	
	.menu-card {
		background-color: #fff;
		border-radius: 12rpx;
		margin: 20rpx;
		padding: 10rpx 30rpx;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
	}
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		padding: 30rpx 30rpx 20rpx;
	}
	
	/* 社区菜单样式 */
	.community-item {
		display: flex;
		align-items: center;
		padding: 24rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
	}
	
	.community-item:last-child {
		border-bottom: none;
	}
	
	.community-icon {
		width: 80rpx;
		height: 80rpx;
		background-color: #ecf5ff;
		border-radius: 40rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 20rpx;
		position: relative;
	}
	
	.message-icon {
		background-color: #ffe8e8;
	}
	
	.event-icon {
		background-color: #f0f9eb;
	}
	
	.community-icon .iconfont {
		font-size: 40rpx;
		color: #007AFF;
	}
	
	.message-icon .iconfont {
		color: #ff6b6b;
	}
	
	.event-icon .iconfont {
		color: #67c23a;
	}
	
	.badge {
		position: absolute;
		top: -6rpx;
		right: -6rpx;
		min-width: 30rpx;
		height: 30rpx;
		line-height: 30rpx;
		text-align: center;
		background-color: #ff4d4f;
		color: #fff;
		border-radius: 15rpx;
		font-size: 20rpx;
		padding: 0 6rpx;
	}
	
	.community-info {
		flex: 1;
	}
	
	.community-title {
		font-size: 28rpx;
		color: #333;
		font-weight: bold;
		margin-bottom: 6rpx;
		display: block;
	}
	
	.community-count {
		font-size: 24rpx;
		color: #999;
		display: block;
	}
	
	.icon-right {
		font-size: 24rpx;
		color: #ccc;
	}
	
	/* 话题列表样式 */
	.topic-list {
		padding: 0 20rpx;
	}
	
	.topic-item {
		display: flex;
		background-color: #fff;
		border-radius: 12rpx;
		margin-bottom: 20rpx;
		padding: 20rpx;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
	}
	
	.topic-image {
		width: 160rpx;
		height: 120rpx;
		border-radius: 8rpx;
		margin-right: 20rpx;
	}
	
	.topic-info {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
	
	.topic-title {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
	}
	
	.topic-meta {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	
	.topic-tag {
		font-size: 24rpx;
		color: #007AFF;
	}
	
	.topic-count {
		font-size: 24rpx;
		color: #999;
	}
	
	/* 动态列表样式 */
	.post-list {
		padding: 0 20rpx;
	}
	
	.post-item {
		background-color: #fff;
		border-radius: 12rpx;
		padding: 20rpx;
		margin-bottom: 20rpx;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
	}
	
	.post-header {
		display: flex;
		align-items: center;
		margin-bottom: 20rpx;
	}
	
	.post-avatar {
		width: 80rpx;
		height: 80rpx;
		border-radius: 40rpx;
		margin-right: 20rpx;
	}
	
	.post-user-info {
		flex: 1;
	}
	
	.post-username {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
		display: block;
	}
	
	.post-time {
		font-size: 24rpx;
		color: #999;
	}
	
	.post-content {
		font-size: 28rpx;
		color: #333;
		line-height: 1.5;
		margin-bottom: 20rpx;
	}
	
	.post-images {
		display: flex;
		flex-wrap: wrap;
		margin: 0 -5rpx 20rpx;
	}
	
	.post-image {
		width: calc(33.33% - 10rpx);
		height: 200rpx;
		margin: 5rpx;
		border-radius: 8rpx;
	}
	
	.post-actions {
		display: flex;
		border-top: 1rpx solid #f0f0f0;
		padding-top: 15rpx;
	}
	
	.post-action {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #666;
	}
	
	.post-action .iconfont {
		font-size: 36rpx;
		margin-right: 6rpx;
	}
	
	.action-count {
		font-size: 24rpx;
	}
	
	/* 悬浮按钮 */
	.float-btn {
		position: fixed;
		right: 30rpx;
		bottom: 100rpx;
		width: 100rpx;
		height: 100rpx;
		background-color: #007AFF;
		color: #fff;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 6rpx 20rpx rgba(0, 122, 255, 0.3);
		z-index: 99;
	}
	
	.float-btn .iconfont {
		font-size: 50rpx;
	}
</style> 