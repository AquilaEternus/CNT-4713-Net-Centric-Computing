<?php
    /*Library used for RSA implementation from http://phpseclib.sourceforge.net/*/
    set_include_path(get_include_path() . PATH_SEPARATOR . 'phpseclib1.0.16');
    include_once('Crypt/RSA.php');

    //Declare variables to store plaintext/cipher post data
    $plainText = '';
    $cipherText = '';

    //Create RSA object for use and retrive keys from associative array $keys
    $rsa = new Crypt_RSA();
    $rsa->loadKey('...');
    $rsa->setPrivateKeyFormat(CRYPT_RSA_PRIVATE_FORMAT_PKCS1);
    $rsa->setPublicKeyFormat(CRYPT_RSA_PUBLIC_FORMAT_PKCS1);
    $keys=$rsa->createKey(2048);
    $privateKey=$keys['privatekey'];
    $publicKey=$keys['publickey'];

    //Encrypts data from plain_text textarea using public key
	if(!empty($_POST['submitPlain'])){
		$plainText = htmlspecialchars($_POST['plain_text']);
        $rsa->loadKey($publicKey);
        $rsa->setEncryptionMode(CRYPT_RSA_ENCRYPTION_PKCS1);
        $cipherText = $rsa->encrypt($plainText);
        $cipherText = base64_encode($cipherText);
    }
    //Decrypts data from cipher_text textarea using private key
    if(!empty($_POST['submitCipher'])){
		$cipherText = htmlspecialchars($_POST['cipher_text']);
        $rsa->loadKey($privateKey);
        $plainText = $rsa->decrypt(base64_decode($cipherText));
    }
?>
<?php include('inc/header.php'); ?>
    <div class="container">
      <br>
      <form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
	      <div class="form-group">
	      	<label>Message to Encrypt:</label>
	      	<textarea name="plain_text" class="form-control" value ="<?php echo $plainText; ?>"></textarea>
	      </div>
	      <input type="submit" name="submitPlain" class="btn btn-primary" value="Encrypt"/>
          <br>
          <br>
          <br>
          <div class="form-group">
	      	<label>Cipher to Decrypt:</label>
	      	<textarea name="cipher_text" class="form-control"><?php echo base64_encode($cipherText); ?></textarea>
	      </div>
	      <input type="submit" name="submitCipher" class="btn btn-primary" value="Decrypt"/>
      </form>
      <p></p>
    </div>
<?php include('inc/footer.php') ?>
