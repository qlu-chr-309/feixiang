<template>
	<view class="my-posts-container">
		<view class="header">
			<view class="back-btn" @click="goBack">
				<text class="iconfont icon-back"></text>
			</view>
			<view class="header-title">我发布的</view>
		</view>
		
		<view class="tabs">
			<view 
				class="tab-item" 
				:class="{ active: activeTab === 'posts' }" 
				@click="switchTab('posts')"
			>
				内容发布
			</view>
			<view 
				class="tab-item" 
				:class="{ active: activeTab === 'questions' }" 
				@click="switchTab('questions')"
			>
				问题咨询
			</view>
			<view 
				class="tab-item" 
				:class="{ active: activeTab === 'comments' }" 
				@click="switchTab('comments')"
			>
				我的评论
			</view>
		</view>
		
		<view class="content-list" v-if="activeTab === 'posts'">
			<view class="post-item" v-for="(item, index) in myPosts" :key="index">
				<view class="post-header">
					<image :src="item.avatar" class="post-avatar"></image>
					<view class="post-user-info">
						<text class="post-username">{{item.username}}</text>
						<text class="post-time">{{item.time}}</text>
					</view>
					<view class="post-options">
						<text class="iconfont icon-more"></text>
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
			
			<view class="empty-state" v-if="myPosts.length === 0">
				<image src="/static/community/empty-posts.png" class="empty-image"></image>
				<text class="empty-text">您还没有发布内容</text>
				<button class="primary-btn" @click="createPost">立即发布</button>
			</view>
		</view>
		
		<view class="content-list" v-if="activeTab === 'questions'">
			<view class="question-item" v-for="(item, index) in myQuestions" :key="index">
				<view class="question-header">
					<text class="question-tag" v-if="item.status === 'answered'">已回答</text>
					<text class="question-tag pending" v-else>待回答</text>
					<text class="question-time">{{item.time}}</text>
				</view>
				<text class="question-title">{{item.title}}</text>
				<text class="question-content">{{item.content}}</text>
				<view class="question-footer">
					<text class="answer-count">{{item.answerCount}}个回答</text>
					<text class="view-count">{{item.viewCount}}次浏览</text>
				</view>
			</view>
			
			<view class="empty-state" v-if="myQuestions.length === 0">
				<image src="/static/community/empty-questions.png" class="empty-image"></image>
				<text class="empty-text">您还没有提问</text>
				<button class="primary-btn" @click="askQuestion">立即提问</button>
			</view>
		</view>
		
		<view class="content-list" v-if="activeTab === 'comments'">
			<view class="comment-item" v-for="(item, index) in myComments" :key="index">
				<view class="comment-header">
					<text class="comment-info">评论了 {{item.targetType}} · {{item.time}}</text>
				</view>
				<text class="comment-content">{{item.content}}</text>
				<view class="comment-target">
					<text class="target-title">{{item.targetTitle}}</text>
				</view>
			</view>
			
			<view class="empty-state" v-if="myComments.length === 0">
				<image src="/static/community/empty-comments.png" class="empty-image"></image>
				<text class="empty-text">您还没有发表评论</text>
			</view>
		</view>
		
		<view class="float-btn" @click="createPost" v-if="activeTab === 'posts'">
			<text class="iconfont icon-add"></text>
		</view>
		
		<view class="float-btn" @click="askQuestion" v-if="activeTab === 'questions'">
			<text class="iconfont icon-add"></text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				activeTab: 'posts',
				myPosts: [
					{
						id: 1,
						username: '我',
						avatar: '/static/community/my-avatar.jpg',
						time: '昨天 15:30',
						content: '今天测试了新入手的大疆Mini 3 Pro，续航和画质都超出预期，分享一组航拍照片，大家感受一下！',
						images: ['/static/community/post1-1.jpg', '/static/community/post1-2.jpg'],
						likeCount: 25,
						commentCount: 8,
						shareCount: 3
					},
					{
						id: 2,
						username: '我',
						avatar: '/static/community/my-avatar.jpg',
						time: '2023-04-05 09:15',
						content: '有没有飞友知道哪里可以报名无人机执照考试？求推荐靠谱的培训机构。',
						images: [],
						likeCount: 12,
						commentCount: 15,
						shareCount: 0
					}
				],
				myQuestions: [
					{
						id: 1,
						title: '大疆Mini 3 Pro是否适合新手入门？',
						content: '作为无人机新手，预算有限，想入手一台Mini 3 Pro，不知道操作难度如何，是否适合新手？',
						time: '3天前',
						status: 'answered',
						answerCount: 5,
						viewCount: 128
					},
					{
						id: 2,
						title: '如何解决无人机信号干扰问题？',
						content: '最近飞行时经常遇到信号干扰，导致图传不稳定，有什么好的解决方案吗？',
						time: '1周前',
						status: 'pending',
						answerCount: 2,
						viewCount: 75
					}
				],
				myComments: [
					{
						id: 1,
						content: '谢谢分享，非常实用的技巧！',
						targetType: '文章',
						targetTitle: '无人机航拍构图技巧详解',
						time: '2023-04-08'
					},
					{
						id: 2,
						content: '我也遇到过这个问题，可以尝试更新固件解决。',
						targetType: '问题',
						targetTitle: '无人机启动后无法正常连接遥控器',
						time: '2023-04-06'
					}
				]
			}
		},
		methods: {
			goBack() {
				uni.navigateBack();
			},
			switchTab(tab) {
				this.activeTab = tab;
			},
			createPost() {
				uni.navigateTo({
					url: '/pages/community/createPost'
				});
			},
			askQuestion() {
				uni.navigateTo({
					url: '/pages/community/askQuestion'
				});
			}
		}
	}
</script>

<style>
	.my-posts-container {
		min-height: 100vh;
		background-color: #f5f5f5;
		padding-bottom: 120rpx;
		position: relative;
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
	
	.content-list {
		padding: 20rpx;
	}
	
	.post-item {
		background-color: #fff;
		border-radius: 12rpx;
		padding: 24rpx;
		margin-bottom: 20rpx;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
	}
	
	.post-header {
		display: flex;
		align-items: center;
		margin-bottom: 16rpx;
	}
	
	.post-avatar {
		width: 80rpx;
		height: 80rpx;
		border-radius: 40rpx;
		margin-right: 16rpx;
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
		display: block;
	}
	
	.post-options {
		color: #999;
		font-size: 40rpx;
	}
	
	.post-content {
		font-size: 28rpx;
		color: #333;
		line-height: 1.6;
		margin-bottom: 16rpx;
	}
	
	.post-images {
		display: flex;
		flex-wrap: wrap;
		margin-bottom: 16rpx;
	}
	
	.post-image {
		width: 220rpx;
		height: 220rpx;
		margin-right: 10rpx;
		margin-bottom: 10rpx;
		border-radius: 8rpx;
	}
	
	.post-actions {
		display: flex;
		border-top: 1rpx solid #f0f0f0;
		padding-top: 16rpx;
	}
	
	.post-action {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #666;
	}
	
	.action-count {
		font-size: 24rpx;
		margin-left: 8rpx;
	}
	
	.question-item {
		background-color: #fff;
		border-radius: 12rpx;
		padding: 24rpx;
		margin-bottom: 20rpx;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
	}
	
	.question-header {
		display: flex;
		justify-content: space-between;
		margin-bottom: 16rpx;
	}
	
	.question-tag {
		font-size: 24rpx;
		color: #52c41a;
		background-color: #f6ffed;
		padding: 6rpx 16rpx;
		border-radius: 30rpx;
	}
	
	.question-tag.pending {
		color: #fa8c16;
		background-color: #fff7e6;
	}
	
	.question-time {
		font-size: 24rpx;
		color: #999;
	}
	
	.question-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 16rpx;
		display: block;
	}
	
	.question-content {
		font-size: 28rpx;
		color: #666;
		margin-bottom: 16rpx;
		display: block;
		line-height: 1.6;
	}
	
	.question-footer {
		display: flex;
		font-size: 24rpx;
		color: #999;
	}
	
	.answer-count {
		margin-right: 24rpx;
	}
	
	.comment-item {
		background-color: #fff;
		border-radius: 12rpx;
		padding: 24rpx;
		margin-bottom: 20rpx;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
	}
	
	.comment-header {
		margin-bottom: 16rpx;
	}
	
	.comment-info {
		font-size: 24rpx;
		color: #999;
	}
	
	.comment-content {
		font-size: 28rpx;
		color: #333;
		line-height: 1.6;
		margin-bottom: 16rpx;
		display: block;
	}
	
	.comment-target {
		background-color: #f5f5f5;
		border-radius: 8rpx;
		padding: 16rpx;
	}
	
	.target-title {
		font-size: 26rpx;
		color: #666;
		display: block;
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
		margin-bottom: 30rpx;
	}
	
	.primary-btn {
		background-color: #007AFF;
		color: #fff;
		font-size: 28rpx;
		padding: 16rpx 40rpx;
		border-radius: 40rpx;
		border: none;
	}
	
	.float-btn {
		position: fixed;
		right: 40rpx;
		bottom: 40rpx;
		width: 100rpx;
		height: 100rpx;
		background-color: #007AFF;
		border-radius: 50rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #fff;
		font-size: 40rpx;
		box-shadow: 0 6rpx 16rpx rgba(0, 122, 255, 0.3);
	}
</style> 