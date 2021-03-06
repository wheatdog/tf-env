"""
Watch random agent play an environment.
"""

import time

from gym.envs.classic_control.rendering import SimpleImageViewer
import tensorflow as tf

from tf_env import Pong


def main():
    env = Pong()
    init_state = env.reset(1)
    states = tf.placeholder(init_state.dtype, shape=init_state.get_shape())
    actions = tf.random_uniform(shape=[1], minval=0, maxval=env.num_actions, dtype=tf.int32)
    new_states, rews, dones = env.step(states, actions)
    image = env.observe(states)
    viewer = SimpleImageViewer()
    with tf.Session() as sess:
        cur_states = sess.run(init_state)
        while True:
            cur_states, cur_rews, cur_dones = sess.run([new_states, rews, dones],
                                                       feed_dict={states: cur_states})
            cur_image = sess.run(image, feed_dict={states: cur_states})
            viewer.imshow(cur_image[0])
            if cur_dones[0]:
                print('done with reward: %f' % cur_rews[0])
            time.sleep(1.0 / 60)


if __name__ == '__main__':
    main()
