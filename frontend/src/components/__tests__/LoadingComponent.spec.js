import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import Loading from '../LoadingComponent.vue'

describe('Loading', () => {
  it('renders default slot when loading and successBadge props are falsy', () => {
    const wrapper = mount(Loading, {
      slots: {
        default: '<div class="test-content"></div>'
      }
    })

    expect(wrapper.find('.test-content').exists()).toBeTruthy()
    expect(wrapper.find('.spinner-wrapper').exists()).toBeFalsy()
    expect(wrapper.find('.success-wrapper').exists()).toBeFalsy()
  })

  it('renders spinner when loading prop is truthy', () => {
    const wrapper = mount(Loading, {
      props: {
        loading: true
      }
    })

    expect(wrapper.find('.spinner-wrapper').exists()).toBeTruthy()
    expect(wrapper.find('.success-wrapper').exists()).toBeFalsy()
  })

  it('renders success icon when successBadge prop is truthy', () => {
    const wrapper = mount(Loading, {
      props: {
        successBadge: true
      }
    })

    expect(wrapper.find('.spinner-wrapper').exists()).toBeFalsy()
    expect(wrapper.find('.success-wrapper').exists()).toBeTruthy()
  })
})
