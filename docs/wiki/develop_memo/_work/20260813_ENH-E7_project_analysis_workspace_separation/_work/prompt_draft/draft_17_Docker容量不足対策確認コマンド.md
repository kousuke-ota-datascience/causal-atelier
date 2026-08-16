# 1. 確認

確認用コマンド

```
echo '=== disk sizes ==='
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS

echo
echo '=== physical volumes ==='
sudo pvs

echo
echo '=== volume groups ==='
sudo vgs

echo
echo '=== logical volumes ==='
sudo lvs

```

確認結果

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ echo '=== disk sizes ==='
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS

echo
echo '=== physical volumes ==='
sudo pvs

echo
echo '=== volume groups ==='
sudo vgs

echo
echo '=== logical volumes ==='
sudo lvs
=== disk sizes ===
NAME                        SIZE FSTYPE      MOUNTPOINTS
loop0                         4K squashfs    /snap/bare/5
loop1                      66.8M squashfs    /snap/core24/1587
loop2                        74M squashfs    /snap/core22/2411
loop3                        74M squashfs    /snap/core22/2292
loop4                      66.8M squashfs    /snap/core24/1643
loop5                     252.4M squashfs    /snap/firefox/8633
loop6                     614.5M squashfs    /snap/gnome-46-2404/164
loop7                      91.7M squashfs    /snap/gtk-common-themes/1535
loop8                       402M squashfs    /snap/mesa-2404/1839
loop9                      50.1M squashfs    /snap/snapd/27591
loop10                     50.1M squashfs    /snap/snapd/27406
sr0                        1024M             
vda                          64G             
├─vda1                        1M             
├─vda2                        2G ext4        /boot
└─vda3                       62G LVM2_member 
  └─ubuntu--vg-ubuntu--lv    31G ext4        /
vdb                          32G             
└─vdb1                       32G ext4        /swap_storage

=== physical volumes ===
[sudo] password for bigbrother: 
  PV         VG        Fmt  Attr PSize   PFree 
  /dev/vda3  ubuntu-vg lvm2 a--  <62.00g 31.00g

=== volume groups ===
  VG        #PV #LV #SN Attr   VSize   VFree 
  ubuntu-vg   1   1   0 wz--n- <62.00g 31.00g

=== logical volumes ===
  LV        VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  ubuntu-lv ubuntu-vg -wi-ao---- <31.00g                            
```


# 2. 拡張実施

## 2.0. 確認結果

```
結論

KVMホスト側で仮想ディスクを拡張する必要はありません。

すでに vda は 64GB あり、そのうち LVM VG ubuntu-vg に 31GB未使用領域があります。

vda                    64G
└─ vda3                62G  LVM PV
   └─ ubuntu-lv        31G  /

LVM側も、

PV      : ~62GB
LV      : ~31GB
PFree   : 31GB
VFree   : 31GB

なので、VM内部だけで / を約31GB → 約62GBへ拡張できます。

実行コマンド
```

## 2.1. 拡張コマンド

```
sudo lvextend -r -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
```

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ sudo lvextend -r -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
  Size of logical volume ubuntu-vg/ubuntu-lv changed from <31.00 GiB (7935 extents) to <62.00 GiB (15871 extents).
  Logical volume ubuntu-vg/ubuntu-lv successfully resized.
resize2fs 1.47.0 (5-Feb-2023)
Filesystem at /dev/mapper/ubuntu--vg-ubuntu--lv is mounted on /; on-line resizing required
old_desc_blocks = 4, new_desc_blocks = 8
The filesystem on /dev/mapper/ubuntu--vg-ubuntu--lv is now 16251904 (4k) blocks long.

```

## 2.2. 完了後確認コマンド

```
echo '=== root filesystem ==='
df -hT /

echo
echo '=== volume group ==='
sudo vgs

echo
echo '=== logical volume ==='
sudo lvs
```

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ echo '=== root filesystem ==='
df -hT /

echo
echo '=== volume group ==='
sudo vgs

echo
echo '=== logical volume ==='
sudo lvs
=== root filesystem ===
Filesystem                        Type  Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv ext4   61G   26G   33G  44% /

=== volume group ===
  VG        #PV #LV #SN Attr   VSize   VFree
  ubuntu-vg   1   1   0 wz--n- <62.00g    0 

=== logical volume ===
  LV        VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  ubuntu-lv ubuntu-vg -wi-ao---- <62.00g             
  ```