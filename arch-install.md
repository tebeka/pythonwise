* cgdisk /dev/sda
    * I do one partition
* mkfs.ext4 /dev/sda1
* mount /dev/sda1 /mnt
* pacstrap -i /mnt base base-devel
* genfstab -U -p /mnt >> /mnt/etc/fstab
* arch-chroot /mnt /bin/bash
* set -o vi
* vi /etc/locale.gen
* locale-gen
* echo LANG=en_US.UTF-8 > /etc/locale.conf
* export LANG=en_US.UTF-8
* ln -s /usr/share/zoneinfo/Asia/Jerusalem /etc/localtime
* hwclock --systohc --utc
* echo HOSTNAME > /etc/hostname
* vi /etc/hosts
    * 127.0.0.1	localhost.localdomain	localhost	myhostname
* pacman -S networkmanager
* systemctl enable NetworkManager
* passwd
* pacman -S gptfdisk syslinux
* syslinux-install_update -i -a -m
* vi /boot/syslinux/syslinux.cfg
    * Change `sda3` to `sda1`
* exit
* umount -R /mnt
* shutdown -h now
* Remove CD from CDROM
* Start
* pacman -S zsh
* useradd -m -G wheel -s /usr/bin/zsh miki
* passwd miki
* pacman -S sudo
* visudo
    * Uncomment line for wheel without password
* pacman -S virtualbox-guest-utils
* depmod
* cat > /etc/modules-load.d/vbox.conf
    vboxguest
    vboxsf
    vboxvideo
* pacman -S xfce4 xfce4-goodies
* pacman -S gdm
* systemctl enable gdm
* REBOOT
