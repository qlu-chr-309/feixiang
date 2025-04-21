<template>
	<view class="ask-question-container">
		<view class="header">
			<view class="back-btn" @click="goBack">
				<text class="iconfont icon-back"></text>
			</view>
			<view class="header-title">提问问题</view>
			<view class="submit-btn" :class="{ disabled: !canSubmit }" @click="submitQuestion">发布</view>
		</view>
		
		<view class="content-area">
			<view class="form-item">
				<text class="form-label">问题标题</text>
				<input 
					type="text" 
					class="title-input" 
					v-model="questionTitle" 
					placeholder="请用一句话简洁描述您的问题"
					maxlength="50"
				/>
				<text class="char-count">{{questionTitle.length}}/50</text>
			</view>
			
			<view class="form-item">
				<text class="form-label">问题详情</text>
				<textarea 
					class="detail-input" 
					v-model="questionDetail" 
					placeholder="详细描述您的问题，以便得到更准确的回答"
					maxlength="1000"
					auto-height
				></textarea>
				<text class="char-count">{{questionDetail.length}}/1000</text>
			</view>
			
			<view class="form-item">
				<text class="form-label">添加图片<text class="optional">(选填)</text></text>
				<view class="image-preview" v-if="images.length > 0">
					<view class="image-item" v-for="(item, index) in images" :key="index">
						<image :src="item" mode="aspectFill" class="preview-image"></image>
						<view class="delete-btn" @click="deleteImage(index)">
							<text class="iconfont icon-close"></text>
						</view>
					</view>
					<view class="add-image-btn" @click="chooseImage" v-if="images.length < 3">
						<text class="iconfont icon-add"></text>
					</view>
				</view>
				<view class="add-image-btn full" @click="chooseImage" v-else>
					<text class="iconfont icon-image"></text>
					<text class="add-text">添加图片（最多3张）</text>
				</view>
			</view>
			
			<view class="form-item">
				<text class="form-label">选择话题</text>
				<view class="selected-topics" v-if="selectedTopics.length > 0">
					<view class="topic-tag" v-for="(item, index) in selectedTopics" :key="index">
						<text>{{item.name}}</text>
						<text class="remove-topic" @click="removeTopic(index)">×</text>
					</view>
					<view class="add-topic-btn" @click="showTopicSelector = true" v-if="selectedTopics.length < 3">
						<text class="iconfont icon-add"></text>
					</view>
				</view>
				<view class="add-topic-btn full" @click="showTopicSelector = true" v-else>
					<text class="iconfont icon-topic"></text>
					<text class="add-text">添加话题（最多3个）</text>
				</view>
			</view>
			
			<view class="post-settings">
				<view class="setting-item">
					<text>匿名提问</text>
					<switch color="#007AFF" :checked="isAnonymous" @change="isAnonymous = $event.detail.value"></switch>
				</view>
			</view>
			
			<view class="tips">
				<text class="tips-title">提问小贴士</text>
				<view class="tips-item">
					<text class="dot">•</text>
					<text>清晰描述问题，提供必要的背景信息</text>
				</view>
				<view class="tips-item">
					<text class="dot">•</text>
					<text>添加相关的话题，帮助问题被合适的人看到</text>
				</view>
				<view class="tips-item">
					<text class="dot">•</text>
					<text>上传图片可以更好地说明问题</text>
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
						<view 
							class="topic-item" 
							v-for="(item, index) in filteredTopics" 
							:key="index" 
							@click="selectTopic(item)"
							:class="{ disabled: isTopicSelected(item) }"
						>
							<text class="topic-name">{{item.name}}</text>
							<text class="topic-count">{{item.count}}人关注</text>
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
				questionTitle: '',
				questionDetail: '',
				images: [],
				selectedTopics: [],
				isAnonymous: false,
				showTopicSelector: false,
				topicSearchText: '',
				topics: [
					{ id: 1, name: '无人机航拍', count: 1284 },
					{ id: 2, name: '无人机测评', count: 873 },
					{ id: 3, name: '飞行技巧', count: 695 },
					{ id: 4, name: '无人机维修', count: 421 },
					{ id: 5, name: '新手教程', count: 569 },
					{ id: 6, name: '植保无人机', count: 326 },
					{ id: 7, name: '大疆无人机', count: 1025 },
					{ id: 8, name: '竞速无人机', count: 287 },
					{ id: 9, name: '多旋翼', count: 453 },
					{ id: 10, name: '固定翼', count: 218 }
				]
			};
		},
		computed: {
			canSubmit() {
				return this.questionTitle.trim() !== '' && this.questionDetail.trim() !== '';
			},
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
				if (this.images.length >= 3) {
					uni.showToast({
						title: '最多只能上传3张图片',
						icon: 'none'
					});
					return;
				}
				
				uni.chooseImage({
					count: 3 - this.images.length,
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
			selectTopic(topic) {
				if (this.selectedTopics.length >= 3) {
					uni.showToast({
						title: '最多只能选择3个话题',
						icon: 'none'
					});
					return;
				}
				
				if (this.isTopicSelected(topic)) {
					uni.showToast({
						title: '该话题已选择',
						icon: 'none'
					});
					return;
				}
				
				this.selectedTopics.push(topic);
				this.showTopicSelector = false;
			},
			removeTopic(index) {
				this.selectedTopics.splice(index, 1);
			},
			isTopicSelected(topic) {
				return this.selectedTopics.some(item => item.id === topic.id);
			},
			validateQuestion() {
				if (!this.questionTitle.trim()) {
					uni.showToast({
						title: '请输入问题标题',
						icon: 'none'
					});
					return false;
				}
				
				if (!this.questionDetail.trim()) {
					uni.showToast({
						title: '请输入问题详情',
						icon: 'none'
					});
					return false;
				}
				
				if (this.selectedTopics.length === 0) {
					uni.showToast({
						title: '请至少选择一个话题',
						icon: 'none'
					});
					return false;
				}
				
				return true;
			},
			submitQuestion() {
				if (!this.validateQuestion()) return;
				
				uni.showLoading({
					title: '发布中...'
				});
				
				// 模拟提交
				setTimeout(() => {
					uni.hideLoading();
					uni.showToast({
						title: '提问成功',
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
	.ask-question-container {
		min-height: 100vh;
		background-color: #f5f5f5;
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
		background-color: #fff;
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
		padding: 20rpx;
	}
	
	.form-item {
		background-color: #fff;
		border-radius: 12rpx;
		padding: 24rpx;
		margin-bottom: 20rpx;
		position: relative;
	}
	
	.form-label {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 16rpx;
		display: block;
	}
	
	.optional {
		font-size: 24rpx;
		color: #999;
		font-weight: normal;
		margin-left: 10rpx;
	}
	
	.title-input {
		width: 100%;
		height: 80rpx;
		font-size: 30rpx;
		color: #333;
		border-bottom: 1rpx solid #f0f0f0;
		padding-bottom: 16rpx;
	}
	
	.detail-input {
		width: 100%;
		font-size: 28rpx;
		line-height: 1.6;
		min-height: 200rpx;
		color: #333;
		margin-bottom: 10rpx;
	}
	
	.char-count {
		font-size: 24rpx;
		color: #999;
		position: absolute;
		right: 24rpx;
		bottom: 24rpx;
	}
	
	.image-preview {
		display: flex;
		flex-wrap: wrap;
	}
	
	.image-item {
		width: 200rpx;
		height: 200rpx;
		margin-right: 20rpx;
		margin-bottom: 20rpx;
		position: relative;
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
		width: 200rpx;
		height: 200rpx;
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
	}
	
	.add-text {
		font-size: 26rpx;
		margin-top: 10rpx;
	}
	
	.selected-topics {
		display: flex;
		flex-wrap: wrap;
	}
	
	.topic-tag {
		height: 64rpx;
		background-color: #f0f7ff;
		border-radius: 32rpx;
		display: flex;
		align-items: center;
		padding: 0 20rpx;
		margin-right: 20rpx;
		margin-bottom: 20rpx;
		font-size: 26rpx;
		color: #007AFF;
	}
	
	.remove-topic {
		margin-left: 10rpx;
		font-size: 32rpx;
	}
	
	.add-topic-btn {
		width: 64rpx;
		height: 64rpx;
		border: 2rpx dashed #ddd;
		border-radius: 32rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #999;
	}
	
	.add-topic-btn.full {
		width: 100%;
		height: 80rpx;
		border-radius: 8rpx;
		display: flex;
		flex-direction: row;
		justify-content: center;
	}
	
	.add-topic-btn.full .iconfont {
		margin-right: 10rpx;
	}
	
	.post-settings {
		background-color: #fff;
		border-radius: 12rpx;
		padding: 0 24rpx;
		margin-bottom: 20rpx;
	}
	
	.setting-item {
		height: 100rpx;
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 28rpx;
		color: #333;
	}
	
	.tips {
		background-color: #fff;
		border-radius: 12rpx;
		padding: 24rpx;
		margin-bottom: 20rpx;
	}
	
	.tips-title {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 16rpx;
		display: block;
	}
	
	.tips-item {
		display: flex;
		margin-bottom: 10rpx;
		font-size: 26rpx;
		color: #666;
		line-height: 1.6;
	}
	
	.dot {
		margin-right: 10rpx;
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
	
	.topic-item.disabled {
		opacity: 0.5;
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