<template>
	<view class="create-post-container">
		<view class="header">
			<view class="back-btn" @click="goBack">
				<text class="iconfont icon-back"></text>
			</view>
			<view class="header-title">发布内容</view>
			<view class="submit-btn" @click="submitPost">发布</view>
		</view>
		
		<view class="content-area">
			<textarea 
				class="post-input" 
				v-model="postContent" 
				placeholder="分享您的无人机体验、技巧或问题..." 
				maxlength="1000"
				auto-height
			></textarea>
			
			<view class="image-preview" v-if="images.length > 0">
				<view class="image-item" v-for="(item, index) in images" :key="index">
					<image :src="item" mode="aspectFill" class="preview-image"></image>
					<view class="delete-btn" @click="deleteImage(index)">
						<text class="iconfont icon-close"></text>
					</view>
				</view>
				<view class="add-image-btn" @click="chooseImage" v-if="images.length < 9">
					<text class="iconfont icon-add"></text>
				</view>
			</view>
			<view class="add-image-btn full" @click="chooseImage" v-else>
				<text class="iconfont icon-image"></text>
				<text class="add-text">添加图片</text>
			</view>
		</view>
		
		<view class="toolbar">
			<view class="tool-item" @click="chooseImage">
				<text class="iconfont icon-image"></text>
				<text>图片</text>
			</view>
			<view class="tool-item" @click="chooseVideo">
				<text class="iconfont icon-video"></text>
				<text>视频</text>
			</view>
			<view class="tool-item" @click="chooseTopic">
				<text class="iconfont icon-topic"></text>
				<text>话题</text>
			</view>
			<view class="tool-item" @click="chooseLocation">
				<text class="iconfont icon-location"></text>
				<text>位置</text>
			</view>
			<view class="tool-item" @click="togglePrivacySettings">
				<text class="iconfont icon-privacy"></text>
				<text>权限</text>
			</view>
		</view>
		
		<view class="post-settings">
			<view class="setting-item">
				<text>同时转发到动态</text>
				<switch color="#007AFF" :checked="settings.shareToFeed" @change="settings.shareToFeed = $event.detail.value"></switch>
			</view>
			<view class="setting-item">
				<text>添加位置信息</text>
				<switch color="#007AFF" :checked="settings.includeLocation" @change="settings.includeLocation = $event.detail.value"></switch>
			</view>
		</view>
		
		<view class="privacy-modal" v-if="showPrivacySettings">
			<view class="modal-mask" @click="showPrivacySettings = false"></view>
			<view class="modal-content">
				<view class="modal-header">
					<text class="modal-title">权限设置</text>
					<view class="close-btn" @click="showPrivacySettings = false">
						<text class="iconfont icon-close"></text>
					</view>
				</view>
				<view class="modal-body">
					<view class="privacy-option" @click="settings.privacy = 'public'">
						<view class="option-icon">
							<text class="iconfont icon-public"></text>
						</view>
						<view class="option-info">
							<text class="option-title">公开</text>
							<text class="option-desc">所有人可见</text>
						</view>
						<view class="radio" :class="{ active: settings.privacy === 'public' }"></view>
					</view>
					<view class="privacy-option" @click="settings.privacy = 'friends'">
						<view class="option-icon">
							<text class="iconfont icon-friends"></text>
						</view>
						<view class="option-info">
							<text class="option-title">仅好友</text>
							<text class="option-desc">仅对您的关注者可见</text>
						</view>
						<view class="radio" :class="{ active: settings.privacy === 'friends' }"></view>
					</view>
					<view class="privacy-option" @click="settings.privacy = 'private'">
						<view class="option-icon">
							<text class="iconfont icon-private"></text>
						</view>
						<view class="option-info">
							<text class="option-title">私密</text>
							<text class="option-desc">仅自己可见</text>
						</view>
						<view class="radio" :class="{ active: settings.privacy === 'private' }"></view>
					</view>
				</view>
				<view class="modal-footer">
					<button class="confirm-btn" @click="confirmPrivacySettings">确定</button>
				</view>
			</view>
		</view>
		
		<view class="topic-modal" v-if="showTopicSelector">
			<view class="modal-mask" @click="showTopicSelector = false"></view>
			<view class="modal-content">
				<view class="modal-header">
					<text class="modal-title">选择话题</text>
					<view class="close-btn" @click="showTopicSelector = false">
						<text class="iconfont icon-close"></text>
					</view>
				</view>
				<view class="modal-body">
					<view class="search-bar">
						<text class="iconfont icon-search"></text>
						<input type="text" placeholder="搜索话题" v-model="topicSearchText" />
					</view>
					<scroll-view scroll-y class="topic-list">
						<view class="topic-item" v-for="(item, index) in filteredTopics" :key="index" @click="selectTopic(item)">
							<text class="topic-name">#{{item.name}}</text>
							<text class="topic-count">{{item.count}}人参与</text>
						</view>
					</scroll-view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				postContent: '',
				images: [],
				showPrivacySettings: false,
				showTopicSelector: false,
				topicSearchText: '',
				settings: {
					privacy: 'public',
					shareToFeed: true,
					includeLocation: false
				},
				topics: [
					{ name: '无人机航拍', count: 1284 },
					{ name: '无人机测评', count: 873 },
					{ name: '飞行技巧', count: 695 },
					{ name: '无人机维修', count: 421 },
					{ name: '新手教程', count: 569 },
					{ name: '植保无人机', count: 326 },
					{ name: '大疆无人机', count: 1025 },
					{ name: '竞速无人机', count: 287 },
					{ name: '多旋翼', count: 453 },
					{ name: '固定翼', count: 218 }
				]
			};
		},
		computed: {
			filteredTopics() {
				if (!this.topicSearchText) {
					return this.topics;
				}
				
				const searchText = this.topicSearchText.toLowerCase();
				return this.topics.filter(topic => 
					topic.name.toLowerCase().includes(searchText)
				);
			}
		},
		methods: {
			goBack() {
				uni.navigateBack();
			},
			chooseImage() {
				if (this.images.length >= 9) {
					uni.showToast({
						title: '最多只能上传9张图片',
						icon: 'none'
					});
					return;
				}
				
				uni.chooseImage({
					count: 9 - this.images.length,
					sizeType: ['compressed'],
					sourceType: ['album', 'camera'],
					success: (res) => {
						this.images = [...this.images, ...res.tempFilePaths];
					}
				});
			},
			deleteImage(index) {
				this.images.splice(index, 1);
			},
			chooseVideo() {
				uni.showToast({
					title: '视频功能开发中',
					icon: 'none'
				});
			},
			chooseTopic() {
				this.showTopicSelector = true;
			},
			selectTopic(topic) {
				this.postContent += ' #' + topic.name + '# ';
				this.showTopicSelector = false;
			},
			chooseLocation() {
				uni.showToast({
					title: '位置功能开发中',
					icon: 'none'
				});
			},
			togglePrivacySettings() {
				this.showPrivacySettings = true;
			},
			confirmPrivacySettings() {
				this.showPrivacySettings = false;
			},
			validatePost() {
				if (!this.postContent.trim()) {
					uni.showToast({
						title: '请输入内容',
						icon: 'none'
					});
					return false;
				}
				
				return true;
			},
			submitPost() {
				if (!this.validatePost()) return;
				
				uni.showLoading({
					title: '发布中...'
				});
				
				// 模拟发布
				setTimeout(() => {
					uni.hideLoading();
					uni.showToast({
						title: '发布成功',
						icon: 'success',
						success: () => {
							setTimeout(() => {
								uni.navigateBack();
							}, 1500);
						}
					});
				}, 1500);
			}
		}
	}
</script>

<style>
	.create-post-container {
		min-height: 100vh;
		background-color: #fff;
		display: flex;
		flex-direction: column;
	}
	
	.header {
		height: 90rpx;
		display: flex;
		align-items: center;
		justify-content: space-between;
		border-bottom: 1rpx solid #f0f0f0;
		padding: 0 30rpx;
	}
	
	.back-btn {
		font-size: 32rpx;
		color: #333;
	}
	
	.header-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
	}
	
	.submit-btn {
		font-size: 30rpx;
		color: #007AFF;
	}
	
	.submit-btn.disabled {
		color: #999;
	}
	
	.content-area {
		flex: 1;
		padding: 30rpx;
	}
	
	.post-input {
		width: 100%;
		font-size: 30rpx;
		line-height: 1.6;
		min-height: 300rpx;
	}
	
	.image-preview {
		display: flex;
		flex-wrap: wrap;
		margin-top: 30rpx;
	}
	
	.image-item {
		width: 210rpx;
		height: 210rpx;
		margin-right: 20rpx;
		margin-bottom: 20rpx;
		position: relative;
	}
	
	.image-item:nth-child(3n) {
		margin-right: 0;
	}
	
	.preview-image {
		width: 100%;
		height: 100%;
		border-radius: 8rpx;
	}
	
	.delete-btn {
		position: absolute;
		top: -15rpx;
		right: -15rpx;
		width: 40rpx;
		height: 40rpx;
		background-color: rgba(0, 0, 0, 0.5);
		color: #fff;
		border-radius: 20rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.add-image-btn {
		width: 210rpx;
		height: 210rpx;
		border: 2rpx dashed #ddd;
		border-radius: 8rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		color: #999;
	}
	
	.add-image-btn.full {
		width: 100%;
		margin-top: 30rpx;
	}
	
	.add-text {
		font-size: 26rpx;
		margin-top: 10rpx;
	}
	
	.toolbar {
		height: 100rpx;
		display: flex;
		align-items: center;
		border-top: 1rpx solid #f0f0f0;
		padding: 0 30rpx;
	}
	
	.tool-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-right: 60rpx;
		font-size: 24rpx;
		color: #666;
	}
	
	.tool-item .iconfont {
		font-size: 48rpx;
		margin-bottom: 6rpx;
	}
	
	.post-settings {
		padding: 0 30rpx;
		border-top: 1rpx solid #f0f0f0;
	}
	
	.setting-item {
		height: 100rpx;
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 28rpx;
		color: #333;
		border-bottom: 1rpx solid #f0f0f0;
	}
	
	.setting-item:last-child {
		border-bottom: none;
	}
	
	.modal-mask {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5);
		z-index: 1000;
	}
	
	.modal-content {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		background-color: #fff;
		border-radius: 24rpx 24rpx 0 0;
		z-index: 1001;
		overflow: hidden;
	}
	
	.modal-header {
		height: 90rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		border-bottom: 1rpx solid #f0f0f0;
	}
	
	.modal-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
	}
	
	.close-btn {
		position: absolute;
		right: 30rpx;
		font-size: 32rpx;
		color: #999;
	}
	
	.modal-body {
		padding: 30rpx;
		max-height: 70vh;
	}
	
	.privacy-option {
		display: flex;
		align-items: center;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
	}
	
	.privacy-option:last-child {
		border-bottom: none;
	}
	
	.option-icon {
		width: 80rpx;
		height: 80rpx;
		background-color: #f5f5f5;
		border-radius: 40rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 20rpx;
	}
	
	.option-icon .iconfont {
		font-size: 40rpx;
		color: #007AFF;
	}
	
	.option-info {
		flex: 1;
	}
	
	.option-title {
		font-size: 30rpx;
		color: #333;
		margin-bottom: 6rpx;
		display: block;
	}
	
	.option-desc {
		font-size: 26rpx;
		color: #999;
		display: block;
	}
	
	.radio {
		width: 40rpx;
		height: 40rpx;
		border-radius: 20rpx;
		border: 2rpx solid #ddd;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.radio.active {
		border-color: #007AFF;
	}
	
	.radio.active::after {
		content: '';
		width: 24rpx;
		height: 24rpx;
		border-radius: 12rpx;
		background-color: #007AFF;
	}
	
	.modal-footer {
		padding: 30rpx;
	}
	
	.confirm-btn {
		height: 80rpx;
		line-height: 80rpx;
		background-color: #007AFF;
		color: #fff;
		font-size: 30rpx;
		border-radius: 40rpx;
	}
	
	.search-bar {
		display: flex;
		align-items: center;
		background-color: #f5f5f5;
		border-radius: 30rpx;
		padding: 15rpx 20rpx;
		margin-bottom: 20rpx;
	}
	
	.search-bar .iconfont {
		color: #999;
		margin-right: 10rpx;
	}
	
	.search-bar input {
		flex: 1;
		height: 60rpx;
		font-size: 28rpx;
	}
	
	.topic-list {
		max-height: 60vh;
	}
	
	.topic-item {
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.topic-name {
		font-size: 28rpx;
		color: #333;
	}
	
	.topic-count {
		font-size: 24rpx;
		color: #999;
	}
</style> 