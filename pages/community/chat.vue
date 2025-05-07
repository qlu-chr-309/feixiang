<template>
	<view class="chat-container">
		<view class="header">
			<view class="back-btn" @click="goBack">
				<text class="iconfont icon-back"></text>
			</view>
			<view class="header-title">{{chatUsername}}</view>
			<view class="more-btn" @click="showMoreOptions">
				<text class="iconfont icon-more"></text>
			</view>
		</view>
		
		<scroll-view 
			scroll-y 
			class="message-list" 
			:scroll-top="scrollTop"
			:scroll-with-animation="true"
			@scrolltoupper="loadMoreMessages"
			upper-threshold="50"
			ref="messageScroll"
		>
			<view class="load-more" v-if="hasMoreMessages">
				<text v-if="isLoading">加载中...</text>
				<text v-else @click="loadMoreMessages">加载更多</text>
			</view>
			
			<view class="date-divider" v-if="messages.length > 0">
				<text>{{formatDate(messages[0].timestamp)}}</text>
			</view>
			
			<block v-for="(item, index) in messages" :key="index">
				<view class="date-divider" v-if="index > 0 && shouldShowDate(item, messages[index-1])">
					<text>{{formatDate(item.timestamp)}}</text>
				</view>
				
				<view class="message-item" :class="{ 'message-self': item.isSelf }">
					<image v-if="!item.isSelf" :src="item.avatar" class="avatar"></image>
					<view class="message-content">
						<text class="message-time">{{formatTime(item.timestamp)}}</text>
						<view class="message-bubble" :class="{ 'bubble-self': item.isSelf }">
							<text v-if="item.type === 'text'">{{item.content}}</text>
							<image 
								v-if="item.type === 'image'" 
								:src="item.content" 
								mode="widthFix" 
								class="message-image"
								@tap="previewImage(item.content)"
							></image>
						</view>
					</view>
					<image v-if="item.isSelf" :src="item.avatar" class="avatar"></image>
				</view>
			</block>
		</scroll-view>
		
		<view class="input-area">
			<view class="toolbar">
				<view class="tool-item" @click="switchToVoice">
					<text class="iconfont" :class="isVoiceMode ? 'icon-keyboard' : 'icon-voice'"></text>
				</view>
				<view class="input-wrapper" v-if="!isVoiceMode">
					<input 
						type="text"
						class="message-input"
						v-model="messageText"
						placeholder="输入消息..."
						confirm-type="send"
						@confirm="sendTextMessage"
					/>
				</view>
				<view class="voice-button" v-else @touchstart="startRecording" @touchend="stopRecording" @touchcancel="cancelRecording">
					<text>按住 说话</text>
				</view>
				<view class="tool-item" @click="chooseEmoji">
					<text class="iconfont icon-emoji"></text>
				</view>
				<view class="tool-item" @click="toggleMoreTools">
					<text class="iconfont icon-plus"></text>
				</view>
				<view class="send-btn" v-if="messageText.trim()" @click="sendTextMessage">
					<text>发送</text>
				</view>
			</view>
			
			<view class="more-tools" v-if="showMoreTools">
				<view class="tool-grid">
					<view class="tool-grid-item" @click="chooseImage">
						<view class="tool-icon">
							<text class="iconfont icon-image"></text>
						</view>
						<text class="tool-name">图片</text>
					</view>
					<view class="tool-grid-item" @click="takePhoto">
						<view class="tool-icon">
							<text class="iconfont icon-camera"></text>
						</view>
						<text class="tool-name">拍摄</text>
					</view>
					<view class="tool-grid-item" @click="chooseVideo">
						<view class="tool-icon">
							<text class="iconfont icon-video"></text>
						</view>
						<text class="tool-name">视频</text>
					</view>
					<view class="tool-grid-item" @click="chooseFile">
						<view class="tool-icon">
							<text class="iconfont icon-file"></text>
						</view>
						<text class="tool-name">文件</text>
					</view>
					<view class="tool-grid-item" @click="chooseLocation">
						<view class="tool-icon">
							<text class="iconfont icon-location"></text>
						</view>
						<text class="tool-name">位置</text>
					</view>
					<view class="tool-grid-item" @click="sendContact">
						<view class="tool-icon">
							<text class="iconfont icon-contact"></text>
						</view>
						<text class="tool-name">名片</text>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				chatId: 0,
				chatUsername: '',
				messageText: '',
				isVoiceMode: false,
				showMoreTools: false,
				messages: [],
				hasMoreMessages: true,
				isLoading: false,
				page: 1,
				scrollTop: 0,
				myAvatar: '/static/community/my-avatar.jpg'
			};
		},
		onLoad(options) {
			if (options.id && options.username) {
				this.chatId = options.id;
				this.chatUsername = options.username;
				this.loadInitialMessages();
			}
		},
		methods: {
			goBack() {
				uni.navigateBack();
			},
			loadInitialMessages() {
				// 模拟加载初始消息
				this.messages = [
					{
						id: 1,
						content: '你好，我想请教一下你使用的是什么型号的无人机？',
						type: 'text',
						timestamp: new Date('2023-04-10 09:30:15'),
						isSelf: false,
						avatar: '/static/community/avatar1.jpg'
					},
					{
						id: 2,
						content: '你好，我使用的是大疆 Mini 3 Pro，性价比很高的一款入门级无人机。',
						type: 'text',
						timestamp: new Date('2023-04-10 09:32:25'),
						isSelf: true,
						avatar: this.myAvatar
					},
					{
						id: 3,
						content: '那它的续航时间怎么样？我比较关心电池能用多久。',
						type: 'text',
						timestamp: new Date('2023-04-10 09:35:40'),
						isSelf: false,
						avatar: '/static/community/avatar1.jpg'
					},
					{
						id: 4,
						content: '它的续航时间还不错，标准电池大约34分钟，飞行智能电池Plus可达47分钟。不过实际飞行时间会受到风速、环境温度等因素影响。',
						type: 'text',
						timestamp: new Date('2023-04-10 09:40:12'),
						isSelf: true,
						avatar: this.myAvatar
					},
					{
						id: 5,
						content: '/static/community/post1-1.jpg',
						type: 'image',
						timestamp: new Date('2023-04-10 09:41:30'),
						isSelf: true,
						avatar: this.myAvatar
					},
					{
						id: 6,
						content: '这是我用它拍的一些照片，你可以看看效果',
						type: 'text',
						timestamp: new Date('2023-04-10 09:41:45'),
						isSelf: true,
						avatar: this.myAvatar
					},
					{
						id: 7,
						content: '/static/community/post1-2.jpg',
						type: 'image',
						timestamp: new Date('2023-04-10 09:42:00'),
						isSelf: true,
						avatar: this.myAvatar
					},
					{
						id: 8,
						content: '哇，照片拍得很不错！看来成像质量很好。请问它的抗风能力如何？我所在的地区风比较大。',
						type: 'text',
						timestamp: new Date('2023-04-10 09:45:38'),
						isSelf: false,
						avatar: '/static/community/avatar1.jpg'
					},
					{
						id: 9,
						content: 'Mini 3 Pro可以抵抗5级风，但如果你所在地区风力经常超过这个级别，可能需要考虑更专业的型号。对于初学者来说，建议在风力小的时候飞行比较安全。',
						type: 'text',
						timestamp: new Date('2023-04-11 08:15:22'),
						isSelf: true,
						avatar: this.myAvatar
					}
				];
				
				// 消息加载完成后，滚动到底部
				this.$nextTick(() => {
					this.scrollToBottom();
				});
			},
			loadMoreMessages() {
				if (!this.hasMoreMessages || this.isLoading) return;
				
				this.isLoading = true;
				
				// 模拟加载更多历史消息
				setTimeout(() => {
					if (this.page >= 3) {
						this.hasMoreMessages = false;
					} else {
						const oldMessages = [
							{
								id: 100 + this.page,
								content: '这是更早的消息 ' + this.page,
								type: 'text',
								timestamp: new Date('2023-04-09 15:30:00'),
								isSelf: Math.random() > 0.5,
								avatar: Math.random() > 0.5 ? this.myAvatar : '/static/community/avatar1.jpg'
							}
						];
						
						this.messages = [...oldMessages, ...this.messages];
						this.page++;
					}
					
					this.isLoading = false;
				}, 1000);
			},
			scrollToBottom() {
				// 使用一个很大的值让滚动条到底部
				this.scrollTop = 9999999;
			},
			sendTextMessage() {
				if (!this.messageText.trim()) return;
				
				const newMessage = {
					id: this.messages.length + 1,
					content: this.messageText,
					type: 'text',
					timestamp: new Date(),
					isSelf: true,
					avatar: this.myAvatar
				};
				
				this.messages.push(newMessage);
				this.messageText = '';
				
				// 消息发送完成后，滚动到底部
				this.$nextTick(() => {
					this.scrollToBottom();
				});
				
				// 模拟对方回复
				if (Math.random() > 0.3) {
					setTimeout(() => {
						this.receiveMessage();
					}, 2000 + Math.random() * 3000);
				}
			},
			receiveMessage() {
				const replies = [
					'好的，我明白了',
					'谢谢你的解答！',
					'这个信息很有帮助',
					'我再考虑一下',
					'你的建议很专业',
					'我对这款无人机很感兴趣',
					'价格方面能接受',
					'你飞行多久了？有什么技巧分享吗？'
				];
				
				const randomReply = replies[Math.floor(Math.random() * replies.length)];
				
				const newMessage = {
					id: this.messages.length + 1,
					content: randomReply,
					type: 'text',
					timestamp: new Date(),
					isSelf: false,
					avatar: '/static/community/avatar1.jpg'
				};
				
				this.messages.push(newMessage);
				
				// 消息接收完成后，滚动到底部
				this.$nextTick(() => {
					this.scrollToBottom();
				});
			},
			showMoreOptions() {
				uni.showActionSheet({
					itemList: ['查看资料', '清空聊天记录', '举报', '加入黑名单'],
					success: (res) => {
						if (res.tapIndex === 1) {
							uni.showModal({
								title: '提示',
								content: '确定要清空聊天记录吗？',
								success: (res) => {
									if (res.confirm) {
										this.messages = [];
									}
								}
							});
						}
					}
				});
			},
			switchToVoice() {
				this.isVoiceMode = !this.isVoiceMode;
			},
			startRecording() {
				uni.showToast({
					title: '开始录音',
					icon: 'none'
				});
			},
			stopRecording() {
				uni.showToast({
					title: '录音功能开发中',
					icon: 'none'
				});
			},
			cancelRecording() {
				uni.showToast({
					title: '取消录音',
					icon: 'none'
				});
			},
			chooseEmoji() {
				uni.showToast({
					title: '表情功能开发中',
					icon: 'none'
				});
			},
			toggleMoreTools() {
				this.showMoreTools = !this.showMoreTools;
			},
			chooseImage() {
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'],
					sourceType: ['album'],
					success: (res) => {
						const newMessage = {
							id: this.messages.length + 1,
							content: res.tempFilePaths[0],
							type: 'image',
							timestamp: new Date(),
							isSelf: true,
							avatar: this.myAvatar
						};
						
						this.messages.push(newMessage);
						this.showMoreTools = false;
						
						// 消息发送完成后，滚动到底部
						this.$nextTick(() => {
							this.scrollToBottom();
						});
					}
				});
			},
			takePhoto() {
				uni.showToast({
					title: '拍摄功能开发中',
					icon: 'none'
				});
				this.showMoreTools = false;
			},
			chooseVideo() {
				uni.showToast({
					title: '视频功能开发中',
					icon: 'none'
				});
				this.showMoreTools = false;
			},
			chooseFile() {
				uni.showToast({
					title: '文件功能开发中',
					icon: 'none'
				});
				this.showMoreTools = false;
			},
			chooseLocation() {
				uni.showToast({
					title: '位置功能开发中',
					icon: 'none'
				});
				this.showMoreTools = false;
			},
			sendContact() {
				uni.showToast({
					title: '名片功能开发中',
					icon: 'none'
				});
				this.showMoreTools = false;
			},
			previewImage(url) {
				// 找出所有图片消息的URL
				const imageUrls = this.messages
					.filter(msg => msg.type === 'image')
					.map(msg => msg.content);
				
				uni.previewImage({
					current: url,
					urls: imageUrls
				});
			},
			formatDate(timestamp) {
				const date = new Date(timestamp);
				const now = new Date();
				
				const isToday = date.getDate() === now.getDate() && 
							  date.getMonth() === now.getMonth() && 
							  date.getFullYear() === now.getFullYear();
				
				const isYesterday = date.getDate() === now.getDate() - 1 && 
								  date.getMonth() === now.getMonth() && 
								  date.getFullYear() === now.getFullYear();
				
				if (isToday) {
					return '今天';
				} else if (isYesterday) {
					return '昨天';
				} else {
					return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
				}
			},
			formatTime(timestamp) {
				const date = new Date(timestamp);
				return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
			},
			shouldShowDate(currentMsg, prevMsg) {
				const currentDate = new Date(currentMsg.timestamp);
				const prevDate = new Date(prevMsg.timestamp);
				
				return currentDate.getDate() !== prevDate.getDate() || 
					   currentDate.getMonth() !== prevDate.getMonth() || 
					   currentDate.getFullYear() !== prevDate.getFullYear();
			}
		}
	}
</script>

<style>
	.chat-container {
		min-height: 100vh;
		background-color: #f5f5f5;
		display: flex;
		flex-direction: column;
	}
	
	.header {
		height: 90rpx;
		background-color: #007AFF;
		color: #fff;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 30rpx;
	}
	
	.back-btn, .more-btn {
		font-size: 36rpx;
	}
	
	.header-title {
		font-size: 32rpx;
		font-weight: bold;
	}
	
	.message-list {
		flex: 1;
		padding: 20rpx;
		box-sizing: border-box;
		height: calc(100vh - 90rpx - 100rpx);
	}
	
	.load-more {
		text-align: center;
		padding: 20rpx 0;
		font-size: 24rpx;
		color: #999;
	}
	
	.date-divider {
		text-align: center;
		margin: 30rpx 0;
		position: relative;
	}
	
	.date-divider text {
		display: inline-block;
		padding: 0 20rpx;
		background-color: #f5f5f5;
		position: relative;
		z-index: 1;
		font-size: 24rpx;
		color: #999;
	}
	
	.date-divider::before {
		content: '';
		position: absolute;
		left: 0;
		right: 0;
		top: 50%;
		height: 1rpx;
		background-color: #e0e0e0;
		z-index: 0;
	}
	
	.message-item {
		display: flex;
		margin-bottom: 30rpx;
	}
	
	.message-self {
		flex-direction: row-reverse;
	}
	
	.avatar {
		width: 80rpx;
		height: 80rpx;
		border-radius: 40rpx;
		margin: 0 20rpx;
	}
	
	.message-content {
		max-width: 70%;
		display: flex;
		flex-direction: column;
	}
	
	.message-self .message-content {
		align-items: flex-end;
	}
	
	.message-time {
		font-size: 24rpx;
		color: #999;
		margin-bottom: 6rpx;
	}
	
	.message-bubble {
		background-color: #fff;
		border-radius: 10rpx;
		padding: 16rpx 24rpx;
		font-size: 28rpx;
		color: #333;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
		word-break: break-all;
	}
	
	.bubble-self {
		background-color: #007AFF;
		color: #fff;
	}
	
	.message-image {
		max-width: 400rpx;
		border-radius: 10rpx;
	}
	
	.input-area {
		background-color: #f8f8f8;
		border-top: 1rpx solid #e0e0e0;
	}
	
	.toolbar {
		height: 100rpx;
		display: flex;
		align-items: center;
		padding: 0 20rpx;
	}
	
	.tool-item {
		width: 60rpx;
		height: 60rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 48rpx;
		color: #666;
	}
	
	.input-wrapper {
		flex: 1;
		background-color: #fff;
		border-radius: 8rpx;
		margin: 0 20rpx;
		padding: 0 20rpx;
	}
	
	.message-input {
		height: 70rpx;
		font-size: 28rpx;
	}
	
	.voice-button {
		flex: 1;
		height: 70rpx;
		background-color: #fff;
		border-radius: 8rpx;
		margin: 0 20rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #666;
		font-size: 28rpx;
	}
	
	.send-btn {
		height: 60rpx;
		padding: 0 20rpx;
		background-color: #007AFF;
		color: #fff;
		font-size: 28rpx;
		border-radius: 30rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.more-tools {
		background-color: #f8f8f8;
		padding: 30rpx 20rpx;
		border-top: 1rpx solid #e0e0e0;
	}
	
	.tool-grid {
		display: flex;
		flex-wrap: wrap;
	}
	
	.tool-grid-item {
		width: 20%;
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 30rpx;
	}
	
	.tool-icon {
		width: 100rpx;
		height: 100rpx;
		background-color: #fff;
		border-radius: 20rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 10rpx;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
	}
	
	.tool-icon .iconfont {
		font-size: 52rpx;
		color: #007AFF;
	}
	
	.tool-name {
		font-size: 24rpx;
		color: #666;
	}
</style> 