# simple_path_tracer

シンプルなパストレーサーです。
物理現象をシミュレートし、カメラから光線を逆向きに追ったレンダリング画像を生成します。
複数の球から構成される、コーネルボックスの画像を出力します。
640*480の画像をサンプリング数1024でレンダリングすると、pypyを使っても、９時間ぐらいかかります。
標準ライブラリしか使っていないため、以下のコマンドですぐ実行されます。
スクリプトと同じディレクトリ内に、output.ppmというファイルが出力されます。
ppmビュワーで開くと画像が閲覧できます

```
python simple_path_tracer.py
```

## TODO

* 画像が上下逆さまに出力されてしまう
* 高速化
* 単体テストの充実
* コメントの充実
* 最新の手法を取り入れて出力結果を改善する

## 出力サンプル

![output_image](https://github.com/seijik42/simple_path_tracer/blob/master/output/output_1024.png)

## 参照

ほぼこちらのクローンです。
https://github.com/githole/simple-pathtracer
