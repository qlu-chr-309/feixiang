<template>
	<view class="content">
		<image class="logo" :src="droneImage" mode="aspectFill"></image>
		<view class="text-area">
			<text class="title">飞享 - 无人机服务平台</text>
		</view>
        
        <view class="button-group">
            <button class="nav-button login-button" @click="navigateTo('/pages/login/login')">登录/注册</button>
            <button class="nav-button enter-button" @click="navigateTo('/pages/home/home')">进入首页</button>
        </view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: '飞享 - 无人机服务平台',
				// 使用一个公共的无人机图片URL
				droneImage: 'https://img.icons8.com/color/240/null/drone.png',
				// 备用无人机图片列表
				droneImages: [
					'https://img.icons8.com/color/240/null/drone.png',
					'https://img.icons8.com/fluency/240/null/drone.png',
					'https://img.icons8.com/external-flaticons-flat-flat-icons/240/null/external-drone-automation-technology-flaticons-flat-flat-icons.png',
					'https://img.icons8.com/color/240/null/drone-with-camera.png'
				]
			}
		},
		onLoad() {
			// 检查图片是否能加载
			this.checkImageLoaded();
		},
		methods: {
			navigateTo(url) {
				// 检查是否是tabBar页面
				if (url === '/pages/home/home' || url === '/pages/demand/demand' || 
					url === '/pages/service/service' || url === '/pages/my/my') {
					uni.switchTab({
						url: url
					});
				} else {
					uni.navigateTo({
						url: url
					});
				}
			},
			checkImageLoaded() {
				// 创建图片对象
				const img = new Image();
				img.src = this.droneImage;
				
				// 设置超时
				const timeout = setTimeout(() => {
					// 如果超时，使用备用图片
					this.useBackupImage();
				}, 5000);
				
				// 图片加载失败时
				img.onerror = () => {
					clearTimeout(timeout);
					this.useBackupImage();
				};
				
				// 图片加载成功时
				img.onload = () => {
					clearTimeout(timeout);
					console.log('无人机图片加载成功');
				};
			},
			useBackupImage() {
				// 如果备用图片列表不为空，随机选择一张
				if (this.droneImages.length > 0) {
					// 过滤掉当前已经失败的图片
					const availableImages = this.droneImages.filter(img => img !== this.droneImage);
					if (availableImages.length > 0) {
						// 随机选择一张备用图片
						const randomIndex = Math.floor(Math.random() * availableImages.length);
						this.droneImage = availableImages[randomIndex];
						console.log('使用备用无人机图片');
					} else {
						// 如果没有可用的备用图片，使用本地logo
						this.droneImage = '/static/logo.png';
						console.log('所有无人机图片加载失败，使用本地logo');
					}
				} else {
					// 没有备用图片，使用本地logo
					this.droneImage = '/static/logo.png';
					console.log('无备用无人机图片，使用本地logo');
				}
			}
		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 30rpx;
		height: 100vh;
	}

	.logo {
		height: 240rpx;
		width: 240rpx;
		margin-top: 60rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
		border-radius: 50%;
		box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.1);
		background-color: #f8f8f8; /* 图片加载前的背景色 */
	}

	.text-area {
		display: flex;
		justify-content: center;
		margin-bottom: 80rpx;
	}

	.title {
		font-size: 44rpx;
		font-weight: bold;
		color: #333;
	}
    
    .button-group {
        width: 80%;
        display: flex;
        flex-direction: column;
        gap: 30rpx;
    }
    
    .nav-button {
        height: 100rpx;
        line-height: 100rpx;
        border-radius: 50rpx;
        font-size: 34rpx;
        font-weight: bold;
        letter-spacing: 2rpx;
        box-shadow: 0 6rpx 12rpx rgba(0, 0, 0, 0.1);
    }
    
    .login-button {
        background-color: #FF7F50; /* 珊瑚色 */
        color: white;
    }
    
    .enter-button {
        background-color: #4169E1; /* 皇家蓝 */
        color: white;
    }
</style>
